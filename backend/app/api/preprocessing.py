import spacy
import re
import emoji
from spacy.lang.en.stop_words import STOP_WORDS

# Load spaCy
nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])

# Custom stopwords (keep negations)
custom_stops = STOP_WORDS - {"not", "no", "nor", "never"}

def preprocess(text: str):
    # Normalize text + emojis
    text = re.sub(r"\s+", " ", text).strip()
    text = emoji.demojize(text)  # Convert emojis to text like ':smile:'
    text = re.sub(r"[_:]", " ", text)  # Replace ':' and '_' with spaces
    text = re.sub(r"http\S+|www\S+|@\w+|\d+", "", text)  # Remove URLs, emails, numbers

    # Process doc
    doc = nlp(text)

    tokens = []
    for t in doc:
        token_text = (t.lemma_ if t.lemma_ else t.text).lower().strip()
        if token_text and not (
            t.text.lower() in custom_stops
            or t.is_punct
            or t.like_url
            or t.like_email
        ):
            tokens.append(token_text)

    return {
        "original_text": text,
        "clean_text": " ".join(tokens),
        "tokens": tokens
    }

# ✅ Test
sample = "OMG 🤯 The directors were running late at 9:30!! 😡 But they finally approved it 🎉. Check www.test.com or email me at test@example.com — I’m NOT happy at all!! #fail"
print(preprocess(sample))
