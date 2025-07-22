# agents/macro.py

from utils.data_fetching import fetch_cot_data, fetch_dxy_data, fetch_rate_differential
from utils.data_fetching import fetch_forex_factory_news, fetch_financial_juice_news, fetch_trading_economics_news
from utils.preprocessing import clean_macro_news, parse_macro_news_actionable
from .base import BaseAgent
import traceback

class MacroAgent(BaseAgent):
    name = "macro"

    async def analyze(self):
        try:
            cot = fetch_cot_data()
            dxy = fetch_dxy_data()
            rate_diff = fetch_rate_differential()
            ff_news = fetch_forex_factory_news()
            fj_news = fetch_financial_juice_news()
            te_news = fetch_trading_economics_news()
            news_dict = {
                'forex_factory': ff_news.get('forex_factory_news', ff_news),
                'financial_juice': fj_news.get('financial_juice_news', fj_news),
                'trading_economics': te_news.get('trading_economics_news', te_news)
            }
            cleaned_news = clean_macro_news(news_dict)
            actionable_news = parse_macro_news_actionable(cleaned_news)
            return {
                "cot": cot,
                "dxy": dxy if isinstance(dxy, dict) else "DXY data available as DataFrame",
                "rate_differential": rate_diff,
                "macro_news": cleaned_news,
                "macro_news_actionable": actionable_news
            }
        except Exception as e:
            return {
                "error": str(e),
                "trace": traceback.format_exc()
            } 