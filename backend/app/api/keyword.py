from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.core.keyword_model import extract_keywords

router = APIRouter()

class TextRequest(BaseModel):
    text: str

@router.post("/keywords")
async def get_keywords(request: TextRequest):
    """
    API endpoint to extract keywords from input text.
    """
    keywords = extract_keywords(request.text)
    return {"keywords": keywords}
