# agents/fundamental.py

from utils.data_fetching import fetch_fmp_fundamentals
from .base import BaseAgent
import traceback

class FundamentalAgent(BaseAgent):
    name = "fundamental"

    async def analyze(self):
        try:
            return await fetch_fmp_fundamentals(self.ticker)
        except Exception as e:
            return {
                "error": str(e),
                "trace": traceback.format_exc()
            }
