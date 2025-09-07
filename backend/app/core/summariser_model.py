import logging
from transformers import pipeline

logger = logging.getLogger(__name__)

# Load summarization model locally (no token needed)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary(text: str, max_length: int = 130, min_length: int = 30) -> str:
    """Generate summary using Hugging Face transformers (local model)."""
    if not text:
        raise ValueError("Input text required")

    try:
        result = summarizer(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )
        return result[0]["summary_text"]

    except Exception as e:
        logger.error(f"Summarization failed: {str(e)}")
        raise
