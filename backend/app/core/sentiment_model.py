from transformers import pipeline
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from backend.app.db.supabase_client import store_sentiment_analysis


nltk.download('vader_lexicon', quiet=True, raise_on_error=False)



transformer_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")


vader_analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str):
    try:
        result = transformer_model(text)[0]
        label = result['label']  
        score = result['score']
        
        if score < 0.7:
            return nltk_fallback(text)
        return label, score, score
    except Exception:
        return nltk_fallback(text)

def nltk_fallback(text: str):
    scores = vader_analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.05:
        label = "POSITIVE"
    elif compound <= -0.05:
        label = "NEGATIVE"
    else:
        label = "NEUTRAL"
    confidence = abs(compound)
    return label, compound, confidence

def store_results(comment_id: str, sentiment_score: float, sentiment_label: str, confidence_score: float):
    store_sentiment_analysis(
        comment_id=comment_id,
        sentiment_score=sentiment_score,
        sentiment_label=sentiment_label,
        confidence_score=confidence_score
    )
