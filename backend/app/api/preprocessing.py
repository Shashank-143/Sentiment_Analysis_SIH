import re
import emoji
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True) 
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Custom stopwords (keep negations)
try:
    stop_words = set(stopwords.words('english'))
    custom_stops = stop_words - {"not", "no", "nor", "never"}
except:
    custom_stops = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def preprocess(text: str):
    # Normalize text + emojis
    text = re.sub(r"\s+", " ", text).strip()
    text = emoji.demojize(text)  # Convert emojis to text like ':smile:'
    text = re.sub(r"[_:]", " ", text)  # Replace ':' and '_' with spaces
    text = re.sub(r"http\S+|www\S+|@\w+|\d+", "", text)  # Remove URLs, emails, numbers
    
    # Tokenize
    tokens = word_tokenize(text.lower())
    
    # Process tokens
    processed_tokens = []
    for token in tokens:
        # Skip if stopword, punctuation, or too short
        if (token not in custom_stops and 
            token.isalpha() and 
            len(token) > 1):
            # Lemmatize
            lemmatized = lemmatizer.lemmatize(token, get_wordnet_pos(token))
            processed_tokens.append(lemmatized)
    
    return {
        "original_text": text,
        "clean_text": " ".join(processed_tokens),
        "tokens": processed_tokens
    }

# Test
if __name__ == "__main__":
    sample = "OMG 🤯 The directors were running late at 9:30!! 😡 But they finally approved it 🎉. Check www.test.com or email me at test@example.com – I'm NOT happy at all!! #fail"
    print(preprocess(sample))