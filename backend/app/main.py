from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import summariser, keyword, sentiment, wordcloud, excel_processor
import uvicorn

app = FastAPI(
    title="E-Consultation AI Backend",
    version="1.0.0",
    description="FastAPI backend for sentiment analysis, summarization, keyword extraction, word cloud generation, and Excel processing."
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(summariser.router, prefix="/api", tags=["Summarization"])
app.include_router(keyword.router, prefix="/api", tags=["Keyword Extraction"])
app.include_router(sentiment.router, prefix="/api", tags=["Sentiment Analysis"])
app.include_router(wordcloud.router, prefix="/api", tags=["Word Cloud Generation"])
app.include_router(excel_processor.router, prefix="/api", tags=["Excel Processing"])

@app.get("/status")
async def status():
    return {"message": "E-Consultation AI API is running"}

@app.get("/")
async def root():
    return {"message": "E-Consultation AI Backend", "version": "1.0.0"}

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)