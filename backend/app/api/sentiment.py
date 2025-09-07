from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from backend.app.core.sentiment_model import analyze_sentiment, store_results

router = APIRouter()

class CommentRequest(BaseModel):
    comment_id: str
    text: str

class BatchCommentsRequest(BaseModel):
    comments: List[CommentRequest]

@router.post("/sentiment")
async def sentiment_analysis(request: BatchCommentsRequest):
    results = []
    try:
        for comment in request.comments:
            label, score, confidence = analyze_sentiment(comment.text)
            store_results(
                comment_id=comment.comment_id,
                sentiment_score=score,
                sentiment_label=label,
                confidence_score=confidence
            )
            results.append({
                "comment_id": comment.comment_id,
                "sentiment_label": label,
                "sentiment_score": score,
                "confidence_score": confidence
            })
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {str(e)}")
