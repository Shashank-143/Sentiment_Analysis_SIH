from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import summariser, keyword, sentiment, wordcloud, excel_processor
import uvicorn

app = FastAPI(
    title="E-Consultation AI Backend",
    version="1.0.0",
    description="FastAPI backend for sentiment analysis, summarization, keyword extraction, word cloud generation, and Excel processing."
)

# Add CORS middleware with explicit origins
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://sentiment-analysis-sih.vercel.app",
    "https://sentiment-analysis-sih-frontend.vercel.app",  # Additional production domain
    "https://sih.shashankgoel.tech"
    "https://www.sentiment-analysis-sih.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With", "Content-Disposition"],
    expose_headers=["Content-Disposition", "Content-Type", "Content-Length"]  # Important for file downloads
)

app.include_router(summariser.router, prefix="/api", tags=["Summarization"])
app.include_router(keyword.router, prefix="/api", tags=["Keyword Extraction"])
app.include_router(sentiment.router, prefix="/api", tags=["Sentiment Analysis"])
app.include_router(wordcloud.router, prefix="/api", tags=["Word Cloud Generation"])
app.include_router(excel_processor.router, prefix="/api", tags=["Excel Processing"])

@app.get("/status")
async def status():
    return {"message": "E-Consultation AI API is running", "status": "ok"}

@app.get("/api/status")
async def api_status():
    return {"message": "E-Consultation AI API is running", "status": "ok"}

@app.get("/")
async def root():
    return {"message": "E-Consultation AI Backend", "version": "1.0.0"}

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)