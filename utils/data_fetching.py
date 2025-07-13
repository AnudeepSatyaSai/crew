# utils/data_fetching.py

import asyncio
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import yfinance as yf
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



FMP_API_KEY = "WdHVxeZMbvpg64lyzFiq2YzhTz9aCdg2"
NEWS_API_KEY = "da87ea4c0c194cf8b5e40b4527465cf3"

ALPHA_API_KEY = "A04TIMPH3RPZCVZ5"

async def fetch_alpha_vantage(ticker):
    url = (
        f"https://www.alphavantage.co/query"
        f"?function=TIME_SERIES_DAILY_ADJUSTED"
        f"&symbol={ticker}"
        f"&outputsize=compact"
        f"&apikey={ALPHA_API_KEY}"
    )
    res = await asyncio.to_thread(requests.get, url)
    res.raise_for_status()
    data = res.json()

    if "Time Series (Daily)" in data:
        df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
        df = df.rename(columns=lambda x: x[3:])
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        df = df.astype(float)
        return df

    # Fallback to yfinance
    print("[Info] Alpha Vantage returned no data, falling back to yfinance.")
    return await fetch_yfinance(ticker)

async def fetch_yfinance(ticker):
    def load():
        df = yf.download(ticker, period="6mo", interval="1d", progress=False)
        if df.empty:
            raise ValueError("yfinance returned no data.")
        return df

    df = await asyncio.to_thread(load)
    return df



async def fetch_fmp_fundamentals(ticker):
    url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={FMP_API_KEY}"
    res = await asyncio.to_thread(requests.get, url)
    res.raise_for_status()
    data = res.json()
    if not data:
        raise ValueError("No FMP data")
    return data[0]

async def fetch_news_sentiment(ticker):
    url = (
        f"https://newsapi.org/v2/everything"
        f"?qInTitle={ticker}"
        f"&from={datetime.utcnow().date()}"
        f"&sortBy=relevancy"
        f"&language=en"
        f"&pageSize=20"
        f"&apiKey={NEWS_API_KEY}"
    )
    res = await asyncio.to_thread(requests.get, url)
    res.raise_for_status()
    data = res.json()
    analyzer = SentimentIntensityAnalyzer()
    scores = [analyzer.polarity_scores(article["title"])["compound"] for article in data.get("articles", [])]
    return {
        "news_count": len(scores),
        "average_sentiment": float(np.mean(scores)) if scores else 0,
        "sample_titles": [a["title"] for a in data.get("articles", [])[:3]]
    }
