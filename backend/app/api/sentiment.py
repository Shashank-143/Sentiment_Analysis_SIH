from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from core.sentiment_model import analyze_sentiment, store_results, analyze_sentiment_vader
import logging
import socket
import httpx

router = APIRouter()
logger = logging.getLogger(__name__)

class CommentRequest(BaseModel):
    comment_id: str
    text: str

class BatchCommentsRequest(BaseModel):
    comments: List[CommentRequest]

@router.post("/sentiment")
async def sentiment_analysis(request: BatchCommentsRequest):
    """
    API endpoint for batch sentiment analysis of comments.
    """
    results = []
    try:
        for comment in request.comments:
            try:
                label, score, confidence = await analyze_sentiment(comment.text)

            except (socket.gaierror, ConnectionError, httpx.ConnectError, httpx.ConnectTimeout) as network_err:
                logger.warning(f"Network error encountered, using VADER fallback: {str(network_err)}")
                label, score, confidence = analyze_sentiment_vader(comment.text)
            
            results.append({
                "comment_id": comment.comment_id,
                "sentiment_label": label,
                "sentiment_score": score,
                "confidence_score": confidence
            })
            
            try:
                store_results(
                    comment_id=comment.comment_id,
                    sentiment_score=score,
                    sentiment_label=label,
                    confidence_score=confidence
                )

            except Exception as storage_err:
                logger.error(f"Failed to store results: {str(storage_err)}")
                
        return {"results": results}
    
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {str(e)}")