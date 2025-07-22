# main.py
import asyncio
import json
from datetime import datetime, timezone
import sys

from integrations.interface import TradingInterface
from analysis import patterns
from backtesting.engine import BacktestEngine
from paper_trading.simulator import PaperTradingSimulator

# Original agent imports
from agents.quantitative import QuantitativeAgent
from agents.technical import TechnicalAgent
from agents.sentiment import SentimentAgent
from agents.prediction import PricePredictionAgent
from agents.fundamental import FundamentalAgent
from agents.volatility import VolatilityAgent
from agents.execution import ExecutionAgent
from agents.llm import LLMAgent
from agents.macro import MacroAgent
from agents.medium_frequency import MediumFrequencyAgent
from agents.high_frequency import HighFrequencyAgent
from llm.recommend import llm_explain
from analysis.signals import generate_trade_signals
from explainability.shap_explain import explain_with_shap
from utils.tradingview_snapshot import capture_tradingview_snapshot

AGENT_CLASSES = [
    QuantitativeAgent,
    TechnicalAgent,
    SentimentAgent,
    PricePredictionAgent,
    FundamentalAgent,
    VolatilityAgent,
    ExecutionAgent,
    MacroAgent,
    MediumFrequencyAgent,
    HighFrequencyAgent,
]

def save_llm_training_data(context, summary, path='llm_training_data.jsonl'):
    """Append context and LLM summary to a JSONL file for future fine-tuning."""
    import json
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({'context': context, 'summary': summary}) + '\n')

def save_snapshot_label(img_path, signal, csv_path="snapshot_labels.csv"):
    """Append image path and signal label to a CSV file for training."""
    with open(csv_path, "a") as f:
        f.write(f"{img_path},{signal}\n")

def menu():
    print("\nSelect an option:")
    print("1. Live Trading (MT5)")
    print("2. Live Trading (cTrader)")
    print("3. Backtesting with CSV")
    print("4. Paper Trading Simulation")
    print("5. Run Original Agent Pipeline")
    print("0. Exit")
    return input("Enter choice: ").strip()

async def run_full_pipeline(ticker: str):
    context = {"ticker": ticker}
    agents = [cls(ticker) for cls in AGENT_CLASSES]
    results = await asyncio.gather(*(agent.analyze() for agent in agents), return_exceptions=True)
    for agent, result in zip(agents, results):
        context[agent.name] = result if not isinstance(result, Exception) else {"error": str(result)}
    llm_agent = LLMAgent(context)
    context["llm_summary"] = llm_agent.summarize()
    context["llm_factors"] = llm_agent.generate_factors()
    context["timestamp"] = datetime.now(timezone.utc).isoformat()
    # --- Advanced signal generation ---
    import pandas as pd
    df = pd.DataFrame({k: v for k, v in context.items() if isinstance(v, dict) and 'close' in v}, dtype=float)
    if not df.empty:
        signals_df = generate_trade_signals(df)
        context['advanced_signals'] = signals_df.to_dict(orient='list')
        # SHAP explainability (example for RandomForest)
        try:
            from ml.advanced_models import AdvancedPatternRecognizer
            recognizer = AdvancedPatternRecognizer()
            features = signals_df[['ma_cross', 'breakout']].fillna(0)
            y = (signals_df['ma_cross'] > 0).astype(int)
            recognizer.train_rf(features, y)
            explain_with_shap(recognizer.rf, features)
        except Exception as e:
            print(f"SHAP explainability error: {e}")
    # --- TradingView snapshot ---
    try:
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Example: use the last signal as the label
        signal = signals_df['ensemble_signal'].iloc[-1] if not signals_df.empty else 'hold'
        img_path = f"snapshots/{context['ticker']}_{ts}_{signal}.png"
        capture_tradingview_snapshot(symbol=context['ticker'], save_path=img_path)
        print(f"TradingView snapshot saved to {img_path}")
        save_snapshot_label(img_path, signal)
    except Exception as e:
        print(f"TradingView snapshot error: {e}")
    # --- LLM explanation ---
    try:
        llm_summary = llm_explain(context)
        print("\nLLM Recommendation/Explanation:\n", llm_summary)
        save_llm_training_data(context, llm_summary)
    except Exception as e:
        print(f"Error running LLM explanation: {e}")
    print("\n[INFO] You can visualize results with: streamlit run dashboards/streamlit_dashboard.py")
    return context

def live_trading_demo():
    print("\n--- Live Trading Demo (MT5) ---")
    # WARNING: For security, do not hardcode real credentials in production!
    import MetaTrader5 as mt5

    path = "C:/Program Files/MetaTrader 5/terminal64.exe"  # Update this if needed

    if not mt5.initialize(path):
        print("initialize() failed, error code =", mt5.last_error())
        quit()

    login = 109628
    password = "YOUR_PASSWORD"
    server = "BrokerName-Demo"

    if not mt5.login(login, password, server):
        print("login() failed, error code =", mt5.last_error())
        mt5.shutdown()
        quit()
    else:
        print("Login successful!")

    mt5.shutdown()

    # The original code had a connection attempt here, but the new code handles it.
    # Keeping the original print statements for context.
    print("Connected to MT5.")
    print("Account Info:", ti.get_account_info())
    symbol = input("Enter symbol (e.g. EURUSD): ").strip()
    tf = input("Enter timeframe (e.g. mt5.TIMEFRAME_M1): ").strip() or 'mt5.TIMEFRAME_M1'
    from datetime import timedelta
    end = datetime.now()
    start = end - timedelta(days=5)
    timeframe = getattr(mt5, tf, mt5.TIMEFRAME_M1)
    data = ti.get_historical_data(symbol, timeframe, start, end)
    print(f"Fetched {len(data) if data is not None else 0} bars.")
    import pandas as pd
    if data is not None and len(data) > 0:
        df = pd.DataFrame(data)
        signals_df = generate_trade_signals(df)
        print("Advanced signals:", signals_df.head())
        # SHAP explainability (example for RandomForest)
        try:
            from ml.advanced_models import AdvancedPatternRecognizer
            recognizer = AdvancedPatternRecognizer()
            features = signals_df[['ma_cross', 'breakout']].fillna(0)
            y = (signals_df['ma_cross'] > 0).astype(int)
            recognizer.train_rf(features, y)
            explain_with_shap(recognizer.rf, features)
        except Exception as e:
            print(f"SHAP explainability error: {e}")
        # --- TradingView snapshot ---
        try:
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            # Example: use the last signal as the label
            signal = signals_df['ensemble_signal'].iloc[-1]
            img_path = f"snapshots/{symbol}_{ts}_{signal}.png"
            capture_tradingview_snapshot(symbol=symbol, save_path=img_path)
            print(f"TradingView snapshot saved to {img_path}")
            save_snapshot_label(img_path, signal)
        except Exception as e:
            print(f"TradingView snapshot error: {e}")
        # --- LLM explanation for live trading ---
        context = {
            'symbol': symbol,
            'signals': signals_df.to_dict(orient='list'),
            'account_info': ti.get_account_info(),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        try:
            llm_summary = llm_explain(context)
            print("\nLLM Recommendation/Explanation:\n", llm_summary)
            save_llm_training_data(context, llm_summary)
        except Exception as e:
            print(f"Error running LLM explanation: {e}")
    else:
        print("No data fetched.")
    ti.engine.shutdown()

def live_trading_ctrader_demo():
    print("\n--- Live Trading Demo (cTrader) ---")
    client_id = input("cTrader Client ID: ").strip()
    client_secret = input("cTrader Client Secret: ").strip()
    access_token = input("cTrader Access Token (optional): ").strip() or None
    refresh_token = input("cTrader Refresh Token (optional): ").strip() or None
    ti = TradingInterface('ctrader', client_id=client_id, client_secret=client_secret, access_token=access_token, refresh_token=refresh_token)
    try:
        ti.connect()
        print("Connected to cTrader (stub, implement real logic).")
        account_info = ti.get_account_info()
        print("Account Info:", account_info)
        # Example: fetch data and send order (stubs)
        # data = ti.get_historical_data('EURUSD', 'M1', start, end)
        # print("Fetched data (stub):", data)
        # result = ti.send_order('EURUSD', 0.1, 'BUY')
        # print("Order result (stub):", result)
        # --- LLM explanation for cTrader live trading ---
        context = {
            'platform': 'cTrader',
            'account_info': account_info,
            'signals': {'stub': True},
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        try:
            llm_summary = llm_explain(context)
            print("\nLLM Recommendation/Explanation:\n", llm_summary)
            save_llm_training_data(context, llm_summary)
        except Exception as e:
            print(f"Error running LLM explanation: {e}")
    except Exception as e:
        print(f"Error connecting to cTrader: {e}")

def backtesting_demo():
    print("\n--- Backtesting Demo ---")
    csv_path = input("Enter path to CSV file: ").strip()
    engine = BacktestEngine()
    data = engine.load_csv(csv_path)
    print(f"Loaded {len(data)} rows from CSV.")
    # Example: run backtest with moving average cross (stub)
    # results = engine.run_backtest(lambda df: patterns.moving_average_cross(df, 9, 21))
    # print("Backtest results:", results)
    print("Backtest logic not implemented (stub).")
    # --- LLM explanation for backtesting ---
    context = {
        'csv_path': csv_path,
        'data_rows': len(data) if data is not None else 0,
        'timestamp': datetime.now(timezone.utc).isoformat()
    }
    try:
        llm_summary = llm_explain(context)
        print("\nLLM Recommendation/Explanation:\n", llm_summary)
        save_llm_training_data(context, llm_summary)
    except Exception as e:
        print(f"Error running LLM explanation: {e}")

def paper_trading_demo():
    print("\n--- Paper Trading Simulation ---")
    sim = PaperTradingSimulator()
    print("Initial account info:", sim.get_account_info())
    # Example: place a simulated order
    sim.place_order('EURUSD', 1.0, 'buy', 1.1000)
    print("Account after order:", sim.get_account_info())
    print("Paper trading logic not fully implemented (stub).")
    # --- LLM explanation for paper trading ---
    context = {
        'initial_account': 10000,
        'final_account_info': sim.get_account_info(),
        'timestamp': datetime.now(timezone.utc).isoformat()
    }
    try:
        llm_summary = llm_explain(context)
        print("\nLLM Recommendation/Explanation:\n", llm_summary)
        save_llm_training_data(context, llm_summary)
    except Exception as e:
        print(f"Error running LLM explanation: {e}")

def main():
    while True:
        choice = menu()
        if choice == '1':
            live_trading_demo()
        elif choice == '2':
            live_trading_ctrader_demo()
        elif choice == '3':
            backtesting_demo()
        elif choice == '4':
            paper_trading_demo()
        elif choice == '5':
        ticker = input("Enter ticker symbol: ").strip()
        if not ticker:
                print("Ticker symbol cannot be empty.")
                continue
        report = asyncio.run(run_full_pipeline(ticker))
        print(json.dumps(report, indent=2))
        elif choice == '0':
            print("Exiting.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
