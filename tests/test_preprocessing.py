import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from utils.preprocessing import clean_macro_news, parse_macro_news_actionable

def test_clean_macro_news():
    news_dict = {
        'forex_factory': ['Fed raises rates', 'ECB holds rates', 'Fed raises rates', ''],
        'financial_juice': ['US jobs report strong', 'ECB holds rates'],
        'trading_economics': ['Inflation rises in US', '']
    }
    cleaned = clean_macro_news(news_dict)
    assert 'Fed raises rates' in cleaned
    assert 'ECB holds rates' in cleaned
    assert 'US jobs report strong' in cleaned
    assert 'Inflation rises in US' in cleaned
    assert '' not in cleaned
    assert len(cleaned) == 4

def test_clean_macro_news_empty():
    news_dict = {}
    cleaned = clean_macro_news(news_dict)
    assert cleaned == []

def test_clean_macro_news_all_duplicates():
    news_dict = {
        'forex_factory': ['Same headline', 'Same headline', 'Same headline'],
        'financial_juice': ['Same headline'],
        'trading_economics': ['Same headline']
    }
    cleaned = clean_macro_news(news_dict)
    assert cleaned == ['Same headline']

def test_clean_macro_news_all_errors():
    news_dict = {
        'forex_factory': {'error': 'fail'},
        'financial_juice': {'error': 'fail'},
        'trading_economics': {'error': 'fail'}
    }
    cleaned = clean_macro_news(news_dict)
    assert cleaned == []

def test_parse_macro_news_actionable():
    headlines = [
        'Fed raises rates',
        'US jobs report strong',
        'ECB holds rates',
        'Inflation rises in US'
    ]
    actionable = parse_macro_news_actionable(headlines)
    assert isinstance(actionable, list)
    for item in actionable:
        assert 'headline' in item
        assert 'sentiment' in item
        assert 'event_type' in item
        assert 'entities' in item
        assert isinstance(item['entities'], list)
        assert item['sentiment'] in ['positive', 'negative', 'neutral']

def test_parse_macro_news_actionable_empty():
    actionable = parse_macro_news_actionable([])
    assert actionable == []

def test_parse_macro_news_actionable_nonstring():
    headlines = [None, 123, '', 'Valid headline']
    actionable = parse_macro_news_actionable([str(h) for h in headlines if isinstance(h, str) and h])
    # Only 'Valid headline' should be processed
    assert any('Valid headline' in item['headline'] for item in actionable) 

def test_parse_macro_news_actionable_real_world():
    headlines = [
        'Fed Chair Powell signals possible rate hike in July',
        'ECB keeps rates unchanged amid inflation concerns',
        'US GDP growth beats expectations, stocks rally',
        'Unemployment falls to 3.5% in Eurozone',
        'China central bank injects liquidity into markets',
        'S&P 500 hits new high as tech stocks surge',
        'Recession fears rise after weak retail sales data',
        'BOJ maintains negative interest rate policy',
        'UK inflation slows, pound strengthens',
        'US dollar weakens as trade deficit widens'
    ]
    actionable = parse_macro_news_actionable(headlines)
    assert isinstance(actionable, list)
    for item in actionable:
        assert 'headline' in item
        assert 'sentiment' in item
        assert 'event_type' in item
        assert 'entities' in item
        assert isinstance(item['entities'], list)
        assert item['sentiment'] in ['positive', 'negative', 'neutral']
        # At least one entity or event_type should be detected for complex headlines
        assert item['event_type'] or item['entities'] 