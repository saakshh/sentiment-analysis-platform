# main.py - Final Version

import requests
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from transformers import pipeline, logging
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date, timedelta
from pydantic import BaseModel
from typing import List

logging.set_verbosity_error()

# Database Setup
DATABASE_URL = "postgresql://user:password@localhost/sentiment_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class SentimentResult(Base):
    __tablename__ = "sentiment_results"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    headline = Column(String)
    source = Column(String)
    published_at = Column(DateTime)
    sentiment_label = Column(String)
    sentiment_score = Column(Float)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Financial Sentiment Analysis Platform", version="Final")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load ML Model
print("Loading FinBERT model...")
sentiment_analyzer = pipeline("text-classification", model="ProsusAI/finbert")
print("Model loaded successfully!")
NEWS_API_KEY = "29be5c52539c4104aeeac369065478a5"

class SentimentResponse(BaseModel):
    published_at: datetime
    sentiment_label: str
    sentiment_score: float
    class Config:
        orm_mode = True

# --- API Endpoints ---
@app.get("/", response_class=FileResponse)
def read_dashboard():
    return 'index.html'

def process_and_save_articles(db, ticker, articles):
    """Helper function to process and save a list of articles."""
    for article in articles:
        headline = article.get("title")
        if headline:
            exists = db.query(SentimentResult).filter(SentimentResult.headline == headline, SentimentResult.ticker == ticker.upper()).first()
            if not exists:
                sentiment = sentiment_analyzer(headline)[0]
                db_record = SentimentResult(
                    ticker=ticker.upper(),
                    headline=headline,
                    source=article["source"]["name"],
                    published_at=datetime.fromisoformat(article["publishedAt"].replace("Z", "+00:00")),
                    sentiment_label=sentiment['label'],
                    sentiment_score=sentiment['score']
                )
                db.add(db_record)

@app.get("/fetch-news/{ticker}")
def fetch_news_and_backfill(ticker: str):
    """Fetches news for the last 7 days for a given ticker."""
    db = SessionLocal()
    total_articles = 0
    try:
        for i in range(7): # Loop for the last 7 days
            current_day = date.today() - timedelta(days=i)
            date_str = current_day.isoformat()
            url = f"https://newsapi.org/v2/everything?q={ticker}&from={date_str}&to={date_str}&apiKey={NEWS_API_KEY}&language=en&sortBy=popularity"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            articles = data.get("articles", [])
            total_articles += len(articles)
            process_and_save_articles(db, ticker, articles)
        db.commit()
    finally:
        db.close()
    return {"ticker": ticker, "total_articles_fetched": total_articles}

@app.get("/sentiment/{ticker}", response_model=List[SentimentResponse])
def get_sentiment_data(ticker: str):
    """Retrieves all saved sentiment data for a given ticker."""
    db = SessionLocal()
    try:
        results = db.query(SentimentResult).filter(SentimentResult.ticker == ticker.upper()).order_by(SentimentResult.published_at).all()
        return results
    finally:
        db.close()