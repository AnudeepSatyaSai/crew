# utils/data_fetching.py

import asyncio
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import yfinance as yf
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from gs_quant.session import Environment, GsSession
from gs_quant.markets.securities import SecurityMaster
from gs_quant.data import Dataset
from bs4 import BeautifulSoup
import re

# Initialize GS session (requires client id/secret, for demo use Environment.PROD and prompt for credentials)
import os

gs_client_id = os.environ.get('GS_CLIENT_ID')
gs_client_secret = os.environ.get('GS_CLIENT_SECRET')

ALPHA_API_KEY = "P3CCJSVMG21UPYUP"
NEWS_API_KEY = "3abb70798d794cb89cbbeb009a15dcfd"
FMP_API_KEY = "X1EXVNqDzvvP269Yix53x7PniwJaFpzz"

def gs_login():
    if gs_client_id and gs_client_secret:
        GsSession.use(Environment.PROD, gs_client_id, gs_client_secret)
        return True
    return False

# Update fetch_alpha_vantage to use gs-quant as a fallback after yfinance
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
    try:
        return await fetch_yfinance(ticker)
    except Exception as e:
        print(f"[Info] yfinance failed: {e}")
        raise ValueError(f"All data sources failed for {ticker}.")

async def fetch_yfinance(ticker):
    if ticker.upper() == 'EURUSD':
        ticker = 'EURUSD=X'
    def load():
        df = yf.download(ticker, period="6mo", interval="1d", progress=False)
        if not isinstance(df, pd.DataFrame) or df.empty:
            raise ValueError("yfinance returned no data.")
        # Flatten MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join([str(c) for c in col]).strip().lower() for col in df.columns]
        else:
            df.columns = [str(col).lower() for col in df.columns]
        # If columns are like 'close_jpm', 'close_aapl', etc., rename to 'close'
        close_cols = [col for col in df.columns if re.match(r'^close(_.+)?$', col)]
        if close_cols:
            df['close'] = df[close_cols[0]]
        if 'close' not in df.columns:
            print(f"[DEBUG] yfinance columns: {df.columns}")
            raise ValueError(f"yfinance data missing 'close' column. Columns: {df.columns}")
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

def fetch_cot_data():
    # Example: Download COT data from CFTC
    try:
        url = "https://www.cftc.gov/dea/newcot/futures_only_099741.txt"  # EUR futures as example
        res = requests.get(url)
        res.raise_for_status()
        # Parse text file as needed (placeholder)
        return {"cot_raw": res.text[:500]}  # Return first 500 chars as sample
    except Exception as e:
        return {"error": f"COT data fetch failed: {e}"}

def fetch_dxy_data():
    # Example: Use yfinance for DXY, fallback to error if not available
    try:
        import yfinance as yf
        df = yf.download('DX-Y.NYB', period='6mo', interval='1d', progress=False)
        if df.empty:
            raise ValueError("No DXY data from yfinance.")
        return df
    except Exception as e:
        return {"error": f"DXY data fetch failed: {e}"}

def fetch_rate_differential():
    # Placeholder: In production, use FRED or ECB/FED APIs
    try:
        # Example: Use yfinance for US10Y and DE10Y
        import yfinance as yf
        us10y = yf.download('^TNX', period='6mo', interval='1d', progress=False)
        de10y = yf.download('DE10Y-DE.BD', period='6mo', interval='1d', progress=False)
        if us10y.empty or de10y.empty:
            raise ValueError("No bond yield data.")
        # Calculate latest spread
        spread = float(de10y['Close'].iloc[-1] - us10y['Close'].iloc[-1])
        return {"rate_spread": spread}
    except Exception as e:
        return {"error": f"Rate differential fetch failed: {e}"}

def fetch_forex_factory_news():
    try:
        url = 'https://www.forexfactory.com/news'
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        # Example: extract news headlines and timestamps
        news_items = []
        for item in soup.select('.calendar__event-title'):
            headline = item.get_text(strip=True)
            news_items.append(headline)
        return {'forex_factory_news': news_items[:10]}
    except Exception as e:
        return {'error': f'Forex Factory scraping failed: {e}'}

def fetch_financial_juice_news():
    try:
        url = 'https://www.financialjuice.com/home'
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        news_items = []
        for item in soup.select('.news-item .news-content'):
            headline = item.get_text(strip=True)
            news_items.append(headline)
        return {'financial_juice_news': news_items[:10]}
    except Exception as e:
        return {'error': f'Financial Juice scraping failed: {e}'}

def fetch_trading_economics_news():
    try:
        url = 'https://tradingeconomics.com/news'
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        news_items = []
        for item in soup.select('.table .title'):
            headline = item.get_text(strip=True)
            news_items.append(headline)
        return {'trading_economics_news': news_items[:10]}
    except Exception as e:
        return {'error': f'Trading Economics scraping failed: {e}'}
