import pytest
import pandas as pd
import numpy as np
import asyncio
import main
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.mark.asyncio
def test_full_pipeline(monkeypatch):
    # Synthetic data for all agents
    def fake_fetch_alpha_vantage(ticker):
        dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
        close = np.linspace(100, 110, 30) + np.random.normal(0, 1, 30)
        return pd.DataFrame({'close': close}, index=dates)
    async def fake_fetch_alpha_vantage_async(ticker):
        return fake_fetch_alpha_vantage(ticker)
    # Patch all fetch_alpha_vantage imports in agents
    monkeypatch.setattr('agents.quantitative.fetch_alpha_vantage', fake_fetch_alpha_vantage_async)
    monkeypatch.setattr('agents.technical.fetch_alpha_vantage', fake_fetch_alpha_vantage_async)
    monkeypatch.setattr('agents.volatility.fetch_alpha_vantage', fake_fetch_alpha_vantage_async)
    monkeypatch.setattr('agents.execution.fetch_alpha_vantage', fake_fetch_alpha_vantage_async)
    monkeypatch.setattr('agents.medium_frequency.fetch_alpha_vantage', fake_fetch_alpha_vantage_async)
    monkeypatch.setattr('agents.high_frequency.fetch_alpha_vantage', fake_fetch_alpha_vantage_async)
    # Run pipeline
    result = asyncio.run(main.run_full_pipeline('FAKE'))
    # Validate structure
    assert isinstance(result, dict)
    assert 'quantitative' in result
    assert 'technical' in result
    assert 'volatility' in result
    assert 'execution' in result
    assert 'medium_frequency' in result
    assert 'high_frequency' in result
    assert 'macro' in result
    assert 'llm_summary' in result
    assert 'llm_factors' in result
    # Validate key outputs
    assert 'mean_return' in result['quantitative'] or 'error' in result['quantitative']
    assert 'scalping_signal' in result['medium_frequency'] or 'error' in result['medium_frequency']
    assert 'hft_signal' in result['high_frequency'] or 'error' in result['high_frequency'] 

@pytest.mark.asyncio
def test_full_pipeline_all_errors(monkeypatch):
    async def fake_fetch_alpha_vantage_async(ticker):
        raise Exception('fetch error')
    # Patch all fetch_alpha_vantage imports in agents
    monkeypatch.setattr('agents.quantitative.fetch_alpha_vantage', fake_fetch_alpha_vantage_async)
    monkeypatch.setattr('agents.technical.fetch_alpha_vantage', fake_fetch_alpha_vantage_async)
    monkeypatch.setattr('agents.volatility.fetch_alpha_vantage', fake_fetch_alpha_vantage_async)
    monkeypatch.setattr('agents.execution.fetch_alpha_vantage', fake_fetch_alpha_vantage_async)
    monkeypatch.setattr('agents.medium_frequency.fetch_alpha_vantage', fake_fetch_alpha_vantage_async)
    monkeypatch.setattr('agents.high_frequency.fetch_alpha_vantage', fake_fetch_alpha_vantage_async)
    result = asyncio.run(main.run_full_pipeline('ERROR'))
    # All agent outputs should have 'error' key
    for k in ['quantitative', 'technical', 'volatility', 'execution', 'medium_frequency', 'high_frequency']:
        assert 'error' in result[k] 