import os
import httpx
from dotenv import load_dotenv
import logging
import re
import nltk
from nltk.tokenize import sent_tokenize
from typing import List

load_dotenv()
logger = logging.getLogger(__name__)

# Download NLTK data for fallback summarization
nltk.download('punkt', quiet=True, raise_on_error=False)

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
if not HF_API_TOKEN:
    logger.warning("HF_API_TOKEN is missing in .env file, will use fallback summarization")

HF_SUMMARIZER_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"} if HF_API_TOKEN else {}


def fallback_summarize(text: str, max_sentences: int = 3) -> str:
    if not text:
        return ""
    
    sentences = sent_tokenize(text)
    
    if len(sentences) <= max_sentences:
        return text
    
    summary_sentences = [sentences[0]]
    mid_point = len(sentences) // 2
    if mid_point > 0 and mid_point < len(sentences):
        summary_sentences.append(sentences[mid_point])
    
    if len(summary_sentences) < max_sentences and len(sentences) > 2:
        summary_sentences.append(sentences[-1])
    
    step = len(sentences) // max_sentences
    i = step
    while len(summary_sentences) < max_sentences and i < len(sentences):
        if sentences[i] not in summary_sentences:
            summary_sentences.append(sentences[i])
        i += step
    
    return " ".join(summary_sentences)

async def generate_summary(text: str, max_length: int = 130, min_length: int = 30) -> str:
    """Generate summary using Hugging Face API with fallback."""
    if not text:
        return ""

    # If no API token, use fallback immediately
    if not HF_API_TOKEN:
        logger.info("No HF API token available, using fallback summarization")
        return fallback_summarize(text)

    payload = {
        "inputs": text,
        "parameters": {
            "max_length": max_length,
            "min_length": min_length,
            "do_sample": False
        }
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(HF_SUMMARIZER_URL, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

        if isinstance(result, dict) and "error" in result:
            logger.warning(f"Hugging Face API Error: {result['error']}, using fallback")
            return fallback_summarize(text)

        return result[0]["summary_text"]

    except Exception as e:
        logger.warning(f"Summarization API failed: {str(e)}, using fallback")
        return fallback_summarize(text)