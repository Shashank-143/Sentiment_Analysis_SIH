from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.core.summariser_model import generate_summary

router = APIRouter()

class SummarizeRequest(BaseModel):
    text: str
    max_length: int = 130   
    min_length: int = 30

@router.post("/summarise")
async def summarise_text(request: SummarizeRequest):
    try:
        input_length = len(request.text.split())

        if input_length < 40:  
            max_len = 50
            min_len = 5
        else:  
            max_len = request.max_length
            min_len = request.min_length

        summary = await generate_summary(
            request.text,
            max_length=max_len,
            min_length=min_len
        )
        return {"summary": summary}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")

