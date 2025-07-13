# agents/sentiment.py

from utils.data_fetching import fetch_news_sentiment
from .base import BaseAgent

class SentimentAgent(BaseAgent):
    name = "sentiment"

    async def analyze(self):
        return await fetch_news_sentiment(self.ticker)
