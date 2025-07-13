# agents/fundamental.py

from utils.data_fetching import fetch_fmp_fundamentals
from .base import BaseAgent

class FundamentalAgent(BaseAgent):
    name = "fundamental"

    async def analyze(self):
        return await fetch_fmp_fundamentals(self.ticker)
