import os
import httpx
from dotenv import load_dotenv
import logging
from collections import Counter
import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

load_dotenv()
logger = logging.getLogger(__name__)

# Load spaCy for basic processing
try:
    nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
except:
    nlp = None
    logger.warning("spaCy model not found, using basic text processing")

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
if not HF_API_TOKEN:
    logger.warning("HF_API_TOKEN not found, will use basic keyword extraction")

HF_KEYWORD_URL = "https://api-inference.huggingface.co/models/yanekyuk/bert-keyword-extractor"
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"} if HF_API_TOKEN else {}

# Custom stopwords
custom_stops = STOP_WORDS - {"not", "no", "nor", "never"}

def basic_preprocess(text: str):
    """Basic text preprocessing for keyword extraction"""
    if not text:
        return []
    
    # Basic cleaning
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"http\S+|www\S+|@\w+|\d+", "", text)
    text = text.lower()
    
    if nlp:
        # Use spaCy if available
        doc = nlp(text)
        tokens = []
        for token in doc:
            token_text = (token.lemma_ if token.lemma_ else token.text).strip()
            if token_text and not (
                token.text.lower() in custom_stops
                or token.is_punct
                or token.like_url
                or token.like_email
            ):
                tokens.append(token_text)
        return tokens
    else:
        # Basic tokenization
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        return [word for word in words if word not in custom_stops and len(word) > 2]

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
    """Basic keyword extraction using frequency analysis"""
    try:
        tokens = basic_preprocess(text)
        
        if not tokens:
            return []
        
        # Filter for meaningful words
        meaningful_tokens = [
            token for token in tokens 
            if len(token) > 2 and token.isalpha()
        ]
        
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

    try:
        hf_keywords = await extract_keywords_hf_api(text, top_n)
        if hf_keywords:
            return hf_keywords
        
        return extract_keywords_basic(text, top_n)
        
    except Exception as e:
        logger.error(f"Keyword extraction failed: {str(e)}")
        return extract_keywords_basic(text, top_n)