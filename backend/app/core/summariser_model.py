import os
import httpx
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
if not HF_API_TOKEN:
    raise ValueError("HF_API_TOKEN is missing in .env file")

HF_SUMMARIZER_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}


async def generate_summary(text: str, max_length: int = 130, min_length: int = 30) -> str:
    """Generate summary using Hugging Face API."""
    if not text:
        raise ValueError("Input text required")

    payload = {
        "inputs": text,
        "parameters": {
            "max_length": max_length,
            "min_length": min_length,
            "do_sample": False
        }
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(HF_SUMMARIZER_URL, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

        if isinstance(result, dict) and "error" in result:
            raise RuntimeError(f"Hugging Face API Error: {result['error']}")

        return result[0]["summary_text"]

    except Exception as e:
        logger.error(f"Summarization failed: {str(e)}")
        raise
