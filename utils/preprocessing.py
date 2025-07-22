# utils/preprocessing.py

import numpy as np

def safe_float(series):
    try:
        return float(series.iloc[-1]) if not series.empty and not np.isnan(series.iloc[-1]) else None
    except Exception:
        return None

def calculate_metrics(returns):
    try:
        return {
            "mean_return": returns.mean(),
            "volatility": returns.std(),
            "sharpe_ratio": returns.mean() / returns.std() * np.sqrt(252),
            "sortino_ratio": returns.mean() / returns[returns < 0].std() * np.sqrt(252),
            "max_drawdown": ((1 + returns).cumprod() / (1 + returns).cumprod().cummax() - 1).min()
        }
    except Exception:
        return {k: None for k in ["mean_return", "volatility", "sharpe_ratio", "sortino_ratio", "max_drawdown"]}

def clean_macro_news(news_dict):
    """
    Cleans and normalizes macroeconomic news data from multiple sources.
    - Removes duplicates
    - Strips whitespace
    - Filters out empty or very short headlines
    - Deduplicates across sources
    Returns a merged, cleaned list of headlines.
    """
    all_news = []
    for source, headlines in news_dict.items():
        if isinstance(headlines, dict) and 'error' in headlines:
            continue
        if isinstance(headlines, list):
            all_news.extend(headlines)
        elif isinstance(headlines, dict):
            all_news.extend(headlines.values())
    # Clean
    cleaned = [h.strip() for h in all_news if isinstance(h, str) and len(h.strip()) > 10]
    # Deduplicate
    cleaned = list(dict.fromkeys(cleaned))
    return cleaned

def parse_macro_news_actionable(headlines):
    """
    For each headline, extract:
    - sentiment (positive/negative/neutral)
    - event type (rate hike, inflation, GDP, etc.)
    - relevance (FX, stocks, macro)
    - named entities (ORG, GPE, EVENT, etc.)
    Returns a list of dicts with actionable info.
    """
    import re
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    import spacy
    nlp = spacy.load('en_core_web_sm')
    analyzer = SentimentIntensityAnalyzer()
    event_keywords = {
        'rate hike': ['rate hike', 'raise rates', 'increase rates', 'tightening'],
        'rate cut': ['rate cut', 'lower rates', 'decrease rates', 'easing'],
        'inflation': ['inflation', 'cpi', 'ppi', 'consumer price', 'producer price'],
        'gdp': ['gdp', 'growth', 'gross domestic product'],
        'jobs': ['jobs', 'employment', 'unemployment', 'payrolls'],
        'central bank': ['fed', 'ecb', 'boe', 'boj', 'central bank'],
        'fx': ['eurusd', 'usd', 'eur', 'jpy', 'gbp', 'forex', 'currency'],
        'stocks': ['stock', 'equity', 'shares', 'index', 's&p', 'nasdaq', 'dow'],
        'macro': ['macro', 'economy', 'economic', 'recession', 'expansion']
    }
    results = []
    for h in headlines:
        sent = analyzer.polarity_scores(h)
        if sent['compound'] > 0.2:
            sentiment = 'positive'
        elif sent['compound'] < -0.2:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        event_type = None
        relevance = []
        for k, kws in event_keywords.items():
            for kw in kws:
                if re.search(r'\b' + re.escape(kw) + r'\b', h, re.IGNORECASE):
                    if k in ['fx', 'stocks', 'macro']:
                        relevance.append(k)
                    else:
                        event_type = k if not event_type else event_type + ", " + k
        # NER with spaCy
        doc = nlp(h)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        results.append({
            'headline': h,
            'sentiment': sentiment,
            'event_type': event_type,
            'relevance': ', '.join(relevance) if relevance else None,
            'entities': entities
        })
    return results
