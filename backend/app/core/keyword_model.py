import os
import httpx
from dotenv import load_dotenv
import logging
from collections import Counter
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tag import pos_tag

load_dotenv()
logger = logging.getLogger(__name__)

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True) 
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
if not HF_API_TOKEN:
    logger.warning("HF_API_TOKEN not found, will use basic keyword extraction")

HF_KEYWORD_URL = "https://api-inference.huggingface.co/models/yanekyuk/bert-keyword-extractor"
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"} if HF_API_TOKEN else {}

# Custom stopwords
try:
    stop_words = set(stopwords.words('english'))
    custom_stops = stop_words - {"not", "no", "nor", "never"}
except:
    custom_stops = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
    logger.warning("NLTK stopwords not available, using basic stopwords")

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def basic_preprocess(text: str):
    """Basic text preprocessing for keyword extraction using NLTK"""
    if not text:
        return []
    
    # Basic cleaning
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"http\S+|www\S+|@\w+|\d+", "", text)
    text = text.lower()
    
    # Tokenize using NLTK
    tokens = word_tokenize(text)
    
    processed_tokens = []
    for token in tokens:
        # Skip if stopword, not alphabetic, or too short
        if (token not in custom_stops and 
            token.isalpha() and 
            len(token) > 2):
            # Lemmatize
            lemmatized = lemmatizer.lemmatize(token, get_wordnet_pos(token))
            processed_tokens.append(lemmatized)
    
    return processed_tokens

async def extract_keywords_hf_api(text: str, top_n: int = 10):
    """Extract keywords using Hugging Face API"""
    if not HF_API_TOKEN:
        return None
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                HF_KEYWORD_URL,
                headers=headers,
                json={"inputs": text}
            )
            response.raise_for_status()
            result = response.json()
            
        if isinstance(result, list):
            keywords = []
            for item in result[:top_n]:
                if isinstance(item, dict) and 'word' in item:
                    keywords.append(item['word'])
                elif isinstance(item, str):
                    keywords.append(item)
            return keywords
        return None
    except Exception as e:
        logger.error(f"HF API keyword extraction failed: {str(e)}")
        return None

def extract_keywords_basic(text: str, top_n: int = 10):
    """Basic keyword extraction using frequency analysis with NLTK"""
    try:
        tokens = basic_preprocess(text)
        
        if not tokens:
            return []
        
        # Filter for meaningful words (nouns, adjectives, verbs)
        pos_tags = pos_tag(tokens)
        meaningful_tokens = [
            word for word, pos in pos_tags 
            if pos.startswith(('NN', 'JJ', 'VB')) and len(word) > 2
        ]
        
        # If no meaningful tokens found, use all processed tokens
        if not meaningful_tokens:
            meaningful_tokens = tokens
        
        # Get most frequent words as keywords
        word_freq = Counter(meaningful_tokens)
        keywords = [word for word, _ in word_freq.most_common(top_n)]
        
        return keywords
    except Exception as e:
        logger.error(f"Basic keyword extraction failed: {str(e)}")
        return []

def extract_keywords(text: str, top_n: int = 5):
    """
    Extract top keywords from the given text using basic extraction (synchronous version).
    """
    if not text.strip():
        return []

    return extract_keywords_basic(text, top_n)

async def extract_keywords_async(text: str, top_n: int = 5):
    """
    Async version that tries HF API first, then falls back to basic extraction if needed.
    """
    if not text.strip():
        return []

    # Try Hugging Face API first
    hf_keywords = await extract_keywords_hf_api(text, top_n)
    if hf_keywords:
        return hf_keywords
    
    # Fallback to basic extraction
    return extract_keywords_basic(text, top_n)