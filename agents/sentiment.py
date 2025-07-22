# agents/sentiment.py

from utils.data_fetching import fetch_news_sentiment
from .base import BaseAgent
import traceback

class SentimentAgent(BaseAgent):
    name = "sentiment"

    async def analyze(self):
        try:
            return await fetch_news_sentiment(self.ticker)
        except Exception as e:
            return {
                "error": str(e),
                "trace": traceback.format_exc()
            }
