from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.core.keyword_model import extract_keywords

router = APIRouter()

class TextRequest(BaseModel):
    text: str
    top_n: int = 5 

@router.post("/keywords")
async def get_keywords(request: TextRequest):
    """
    API endpoint to extract keywords from input text.
    """
    try:
        keywords = extract_keywords(request.text, top_n=request.top_n)
        return {"keywords": keywords}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Keyword extraction failed: {str(e)}")
