import os
import httpx
from datetime import datetime
from dotenv import load_dotenv
import logging
import json
from typing import Dict, List, Optional, Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.error("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")

BASE_URL = f"{SUPABASE_URL}/rest/v1"

COMMENTS_URL = f"{BASE_URL}/stakeholder_comments"
SENTIMENTS_URL = f"{BASE_URL}/sentiment_analysis"
SUMMARIES_URL = f"{BASE_URL}/comment_summaries"
WORDCLOUD_URL = f"{BASE_URL}/word_cloud_data"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# Store a stakeholder comment on draft legislation.
def store_comment(comment_text: str, legislation_id: str, stakeholder_id: str, section_reference: Optional[str] = None) -> Dict:

    if not comment_text or not legislation_id or not stakeholder_id:
        logger.error("comment_text, legislation_id, and stakeholder_id are required.")
        raise ValueError("Missing required parameters")

    try:
        timestamp = datetime.utcnow().isoformat()
        data = {
            "comment_text": comment_text,
            "legislation_id": legislation_id,
            "stakeholder_id": stakeholder_id,
            "section_reference": section_reference,
            "created_at": timestamp
        }

        with httpx.Client() as client:
            response = client.post(COMMENTS_URL, headers=headers, json=data)
            response.raise_for_status()
            logger.info(f"Comment stored successfully for legislation {legislation_id}.")
            return response.json()
    except Exception as e:
        logger.error(f"Failed to store comment: {str(e)}")
        raise

# Store sentiment analysis results for a comment.
def store_sentiment_analysis(comment_id: str, sentiment_score: float, sentiment_label: str, confidence_score: float,
                            analysis_details: Optional[Dict] = None) -> Dict:

    if not comment_id:
        logger.error("comment_id is required.")
        raise ValueError("Missing required parameters")

    try:
        timestamp = datetime.utcnow().isoformat()
        data = {
            "comment_id": comment_id,
            "sentiment_score": sentiment_score,
            "sentiment_label": sentiment_label,
            "confidence_score": confidence_score,
            "analysis_details": analysis_details,
            "analyzed_at": timestamp
        }

        with httpx.Client(timeout=5.0) as client:
            response = client.post(SENTIMENTS_URL, headers=headers, json=data)
            response.raise_for_status()
            logger.info(f"Sentiment analysis stored successfully for comment {comment_id}.")
            return response.json()
    except httpx.ConnectError:
        logger.error(f"Network connectivity issue when storing sentiment for comment {comment_id}")
        raise RuntimeError("Network connectivity issue when storing data")
    except Exception as e:
        logger.error(f"Failed to store sentiment analysis: {str(e)}")
        raise

# Store a generated summary of stakeholder comments.
def store_summary(legislation_id: str, summary_text: str, summary_type: str, comment_count: int, metadata: Optional[Dict] = None) -> Dict:

    if not legislation_id or not summary_text:
        logger.error("legislation_id and summary_text are required.")
        raise ValueError("Missing required parameters")

    try:
        timestamp = datetime.utcnow().isoformat()
        data = {
            "legislation_id": legislation_id,
            "summary_text": summary_text,
            "summary_type": summary_type,
            "comment_count": comment_count,
            "metadata": metadata,
            "generated_at": timestamp
        }

        with httpx.Client() as client:
            response = client.post(SUMMARIES_URL, headers=headers, json=data)
            response.raise_for_status()
            logger.info(f"Summary stored successfully for legislation {legislation_id}.")
            return response.json()
    except Exception as e:
        logger.error(f"Failed to store summary: {str(e)}")
        raise

# Store word cloud data generated from stakeholder comments.
def store_word_cloud_data(legislation_id: str, word_data: List[Dict], source_type: str, metadata: Optional[Dict] = None) -> Dict:

    if not legislation_id or not word_data:
        logger.error("legislation_id and word_data are required.")
        raise ValueError("Missing required parameters")

    try:
        timestamp = datetime.utcnow().isoformat()
        data = {
            "legislation_id": legislation_id,
            "word_data": word_data,
            "source_type": source_type,
            "metadata": metadata,
            "generated_at": timestamp
        }

        with httpx.Client() as client:
            response = client.post(WORDCLOUD_URL, headers=headers, json=data)
            response.raise_for_status()
            logger.info(f"Word cloud data stored successfully for legislation {legislation_id}.")
            return response.json()
    except Exception as e:
        logger.error(f"Failed to store word cloud data: {str(e)}")
        raise

# Retrieve stakeholder comments for a specific legislation.
def get_comments(legislation_id: str, limit: int = 100, offset: int = 0, filters: Optional[Dict] = None) -> List[Dict]:

    try:
        params = {
            "select": "*",
            "legislation_id": f"eq.{legislation_id}",
            "order": "created_at.desc",
            "limit": limit,
            "offset": offset
        }
        
        if filters:
            params.update(filters)
            
        with httpx.Client() as client:
            response = client.get(COMMENTS_URL, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Failed to retrieve comments: {str(e)}")
        raise

# Retrieve sentiment analysis results.
def get_sentiment_analysis(comment_ids: Optional[List[str]] = None, 
                          legislation_id: Optional[str] = None,
                          limit: int = 100, offset: int = 0) -> List[Dict]:

    try:
        if comment_ids:
            # Format for Postgres 'in' operator
            comment_ids_str = ",".join(comment_ids)
            params = {
                "comment_id": f"in.({comment_ids_str})",
                "limit": limit,
                "offset": offset
            }
        elif legislation_id:
            # This would require a join query in Supabase
            join_url = f"{SENTIMENTS_URL}?select=*,stakeholder_comments(*)&stakeholder_comments.legislation_id=eq.{legislation_id}"
            with httpx.Client() as client:
                response = client.get(join_url, headers=headers)
                response.raise_for_status()
                return response.json()
        else:
            params = {
                "limit": limit,
                "offset": offset,
                "order": "analyzed_at.desc"
            }
            
        with httpx.Client() as client:
            response = client.get(SENTIMENTS_URL, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Failed to retrieve sentiment analysis: {str(e)}")
        raise

# Retrieve generated summaries for a legislation.
def get_summaries(legislation_id: str, summary_type: Optional[str] = None) -> List[Dict]:

    try:
        params = {
            "legislation_id": f"eq.{legislation_id}",
            "order": "generated_at.desc"
        }
        
        if summary_type:
            params["summary_type"] = f"eq.{summary_type}"
            
        with httpx.Client() as client:
            response = client.get(SUMMARIES_URL, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Failed to retrieve summaries: {str(e)}")
        raise

# Retrieve word cloud data for a legislation.
def get_word_cloud_data(legislation_id: str, source_type: Optional[str] = None) -> List[Dict]:

    try:
        params = {
            "legislation_id": f"eq.{legislation_id}",
            "order": "generated_at.desc"
        }
        
        if source_type:
            params["source_type"] = f"eq.{source_type}"
            
        with httpx.Client() as client:
            response = client.get(WORDCLOUD_URL, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Failed to retrieve word cloud data: {str(e)}")
        raise

# Delete a specific comment from the database.
def delete_comment(comment_id: str) -> Dict:

    try:
        delete_url = f"{COMMENTS_URL}?id=eq.{comment_id}"
        with httpx.Client() as client:
            response = client.delete(delete_url, headers=headers)
            response.raise_for_status()
            logger.info(f"Comment {comment_id} deleted successfully.")
            return response.json()
    except Exception as e:
        logger.error(f"Failed to delete comment: {str(e)}")
        raise

# Get aggregate sentiment statistics for a legislation.
def get_aggregate_sentiment(legislation_id: str) -> Dict:
    
    try:
        # This requires custom SQL with PostgREST
        query_params = {
            "select": "count(*),avg(sentiment_score),min(sentiment_score),max(sentiment_score)",
            "stakeholder_comments.legislation_id": f"eq.{legislation_id}"
        }
        
        join_url = f"{SENTIMENTS_URL}?select=*,stakeholder_comments!inner(*)"
        
        with httpx.Client() as client:
            response = client.get(join_url, headers=headers, params=query_params)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Failed to get aggregate sentiment: {str(e)}")
        raise