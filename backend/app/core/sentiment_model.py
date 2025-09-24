import os
import httpx
import socket
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from db.supabase_client import store_sentiment_analysis
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

nltk.download('vader_lexicon', quiet=True, raise_on_error=False)

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
if not HF_API_TOKEN:
    logger.warning("HF_API_TOKEN not found, will use VADER fallback only")

# Updated to use a different sentiment analysis model that's more reliable
HF_SENTIMENT_URL = "https://api-inference.huggingface.co/models/finiteautomata/bertweet-base-sentiment-analysis"
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"} if HF_API_TOKEN else {}

# VADER analyzer as fallback
vader_analyzer = SentimentIntensityAnalyzer()

async def analyze_sentiment_hf_api(text: str):
    """Analyze sentiment using Hugging Face API"""
    if not HF_API_TOKEN:
        return None
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                HF_SENTIMENT_URL, 
                headers=headers, 
                json={"inputs": text}
            )
            response.raise_for_status()
            result = response.json()
            
        if isinstance(result, list) and len(result) > 0:
            # Get the highest scoring label
            best_result = max(result, key=lambda x: x['score'])
            label = best_result['label']
            score = best_result['score']
            return label, score, score
        return None
    except (httpx.ConnectError, httpx.ConnectTimeout, socket.gaierror) as network_err:
        logger.error(f"HF API network error: {str(network_err)}")
        raise
    except Exception as e:
        logger.error(f"HF API sentiment analysis failed: {str(e)}")
        return None

def analyze_sentiment_vader(text: str):
    """VADER sentiment analysis fallback"""
    scores = vader_analyzer.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.05:
        label = "POSITIVE"
    elif compound <= -0.05:
        label = "NEGATIVE"
    else:
        label = "NEUTRAL"
    
    confidence = abs(compound)
    return label, compound, confidence

async def analyze_sentiment(text: str):
    """Main sentiment analysis function with HF API and VADER fallback"""
    try:
        # Try Hugging Face API first
        hf_result = await analyze_sentiment_hf_api(text)
        if hf_result and hf_result[2] >= 0.7:  # High confidence threshold
            return hf_result
        
        # Fallback to VADER
        logger.info("Using VADER fallback due to low confidence or no result from HF API")
        return analyze_sentiment_vader(text)
        
        
    except (httpx.ConnectError, httpx.ConnectTimeout, socket.gaierror):
        # Explicitly handle network errors by using VADER directly
        logger.warning("Network error connecting to HF API, using VADER fallback")
        return analyze_sentiment_vader(text)
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {str(e)}")
        # Final fallback to VADER
        return analyze_sentiment_vader(text)

def nltk_fallback(text: str):
    """Legacy function for backward compatibility"""
    return analyze_sentiment_vader(text)

def store_results(comment_id: str, sentiment_score: float, sentiment_label: str, confidence_score: float):
    """Store sentiment analysis results"""
    store_sentiment_analysis(
        comment_id=comment_id,
        sentiment_score=sentiment_score,
        sentiment_label=sentiment_label,
        confidence_score=confidence_score
    )