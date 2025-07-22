import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import pandas as pd
import numpy as np
import asyncio
from agents.medium_frequency import MediumFrequencyAgent
from agents.high_frequency import HighFrequencyAgent

class DummyAgent:
    def __init__(self, ticker):
        self.ticker = ticker

@pytest.fixture
def synthetic_data():
    # 30 days of synthetic close prices
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
    close = np.linspace(100, 110, 30) + np.random.normal(0, 1, 30)
    df = pd.DataFrame({'close': close}, index=dates)
    return df

@pytest.mark.asyncio
def test_medium_frequency_agent(monkeypatch, synthetic_data):
    async def fake_fetch_alpha_vantage(ticker):
        return synthetic_data.copy()
    monkeypatch.setattr('agents.medium_frequency.fetch_alpha_vantage', fake_fetch_alpha_vantage)
    agent = MediumFrequencyAgent('FAKE')
    result = asyncio.run(agent.analyze())
    assert 'scalping_signal' in result
    assert 'ensemble_predicted_return' in result
    assert isinstance(result['ensemble_predicted_return'], float)

@pytest.mark.asyncio
def test_high_frequency_agent(monkeypatch, synthetic_data):
    async def fake_fetch_alpha_vantage(ticker):
        return synthetic_data.copy()
    monkeypatch.setattr('agents.high_frequency.fetch_alpha_vantage', fake_fetch_alpha_vantage)
    agent = HighFrequencyAgent('FAKE')
    result = asyncio.run(agent.analyze())
    assert 'hft_signal' in result
    assert 'ensemble_predicted_return' in result
    assert isinstance(result['ensemble_predicted_return'], float)

@pytest.mark.asyncio
def test_medium_frequency_agent_empty(monkeypatch):
    async def fake_fetch_alpha_vantage(ticker):
        import pandas as pd
        return pd.DataFrame({'close': []})
    monkeypatch.setattr('agents.medium_frequency.fetch_alpha_vantage', fake_fetch_alpha_vantage)
    agent = MediumFrequencyAgent('FAKE')
    result = asyncio.run(agent.analyze())
    assert 'error' in result

@pytest.mark.asyncio
def test_high_frequency_agent_empty(monkeypatch):
    async def fake_fetch_alpha_vantage(ticker):
        import pandas as pd
        return pd.DataFrame({'close': []})
    monkeypatch.setattr('agents.high_frequency.fetch_alpha_vantage', fake_fetch_alpha_vantage)
    agent = HighFrequencyAgent('FAKE')
    result = asyncio.run(agent.analyze())
    assert 'error' in result

@pytest.mark.asyncio
def test_medium_frequency_agent_constant(monkeypatch):
    async def fake_fetch_alpha_vantage(ticker):
        import pandas as pd
        import numpy as np
        dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
        close = np.ones(30) * 100
        return pd.DataFrame({'close': close}, index=dates)
    monkeypatch.setattr('agents.medium_frequency.fetch_alpha_vantage', fake_fetch_alpha_vantage)
    agent = MediumFrequencyAgent('FAKE')
    result = asyncio.run(agent.analyze())
    assert 'ensemble_predicted_return' in result

@pytest.mark.asyncio
def test_high_frequency_agent_constant(monkeypatch):
    async def fake_fetch_alpha_vantage(ticker):
        import pandas as pd
        import numpy as np
        dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
        close = np.ones(30) * 100
        return pd.DataFrame({'close': close}, index=dates)
    monkeypatch.setattr('agents.high_frequency.fetch_alpha_vantage', fake_fetch_alpha_vantage)
    agent = HighFrequencyAgent('FAKE')
    result = asyncio.run(agent.analyze())
    assert 'ensemble_predicted_return' in result

@pytest.mark.asyncio
def test_medium_frequency_agent_fetch_error(monkeypatch):
    async def fake_fetch_alpha_vantage(ticker):
        raise Exception('fetch error')
    monkeypatch.setattr('agents.medium_frequency.fetch_alpha_vantage', fake_fetch_alpha_vantage)
    agent = MediumFrequencyAgent('FAKE')
    result = asyncio.run(agent.analyze())
    assert 'error' in result

@pytest.mark.asyncio
def test_high_frequency_agent_fetch_error(monkeypatch):
    async def fake_fetch_alpha_vantage(ticker):
        raise Exception('fetch error')
    monkeypatch.setattr('agents.high_frequency.fetch_alpha_vantage', fake_fetch_alpha_vantage)
    agent = HighFrequencyAgent('FAKE')
    result = asyncio.run(agent.analyze())
    assert 'error' in result 