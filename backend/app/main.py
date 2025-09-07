from fastapi import FastAPI
from backend.app.api import summariser, keyword

app = FastAPI(
    title="E-Consultation AI Backend",
    version="1.0.0",
    description="FastAPI backend for sentiment analysis, summarization, and keyword extraction."
)


app.include_router(summariser.router, prefix="/api", tags=["Summarization"])
app.include_router(keyword.router, prefix="/api", tags=["Keyword Extraction"])

@app.get("/")
async def root():
    return {"message": "E-Consultation AI API is running"}
