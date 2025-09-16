from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from core.wordcloud_gen import create_wordcloud

router = APIRouter()

@router.get("/wordcloud")
def generate_wordcloud(sentence: str):
    buffer = create_wordcloud(sentence)
    return StreamingResponse(buffer, media_type="image/png")

class TextInput(BaseModel):
    sentence: str

@router.post("/wordcloud")
def generate_wordcloud_post(data: TextInput):
    buffer = create_wordcloud(data.sentence)
    return StreamingResponse(buffer, media_type="image/png")
