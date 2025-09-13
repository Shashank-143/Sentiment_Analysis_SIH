from fastapi import FastAPI
from api import summariser, keyword, sentiment

app = FastAPI(
    title="E-Consultation AI Backend",
    version="1.0.0",
    description="FastAPI backend for sentiment analysis, summarization, keyword extraction, and word cloud generation."
)

app.include_router(summariser.router, prefix="/api", tags=["Summarization"])
app.include_router(keyword.router, prefix="/api", tags=["Keyword Extraction"])
app.include_router(sentiment.router, prefix="/api", tags=["Sentiment Analysis"])

@app.get("/status")
async def status():
    return {"message": "E-Consultation AI API is running"}

@app.get("/")
async def root():
    return {"message": "E-Consultation AI Backend", "version": "1.0.0"}