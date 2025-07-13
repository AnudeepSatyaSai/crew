# main.py
import asyncio
import json
from agents.quantitative import QuantitativeAgent
from agents.technical import TechnicalAgent
from agents.sentiment import SentimentAgent
from agents.prediction import PricePredictionAgent
from agents.fundamental import FundamentalAgent
from agents.volatility import VolatilityAgent
from agents.execution import ExecutionAgent
from agents.llm import LLMAgent

from datetime import datetime, timezone

async def run_full_pipeline(ticker: str):
    context = {"ticker": ticker}
    
    # Initialize agents
    agents = [
        QuantitativeAgent(ticker),
        TechnicalAgent(ticker),
        SentimentAgent(ticker),
        PricePredictionAgent(ticker),
        FundamentalAgent(ticker),
        VolatilityAgent(ticker),
        ExecutionAgent(ticker),   # Simulate trade execution using qs-quant
    ]
    
    results = await asyncio.gather(*[a.analyze() for a in agents], return_exceptions=True)
    
    for agent, result in zip(agents, results):
        context[agent.name] = result if not isinstance(result, Exception) else {"error": str(result)}
    
    # Generate LLM summary and factor generation
    llm_agent = LLMAgent(context)
    context["llm_summary"] = llm_agent.summarize()
    context["llm_factors"] = llm_agent.generate_factors()
    context["timestamp"] = datetime.now(timezone.utc).isoformat()
    
    return context

if __name__ == "__main__":
    import sys
    ticker = input("Enter ticker symbol: ").strip()
    report = asyncio.run(run_full_pipeline(ticker))
    print(json.dumps(report, indent=2))
