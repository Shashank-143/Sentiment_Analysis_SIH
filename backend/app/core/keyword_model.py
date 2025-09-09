from keybert import KeyBERT

kw_model = KeyBERT(model="all-MiniLM-L6-v2")

def extract_keywords(text: str, top_n: int = 5):
    """
    Extract top keywords from the given text using KeyBERT.

    Args:
        text (str): Input text
        top_n (int): Number of keywords to return

    Returns:
        List[str]: List of top keywords
    """
    if not text.strip():
        return []

    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2), 
        stop_words="english",
        top_n=top_n
    )

    return [kw[0] for kw in keywords]
