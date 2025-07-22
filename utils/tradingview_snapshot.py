from playwright.sync_api import sync_playwright

def capture_tradingview_snapshot(symbol="AAPL", timeframe="1", save_path="snapshot.png"):
    """
    Capture a TradingView chart snapshot for the given symbol and timeframe.
    symbol: e.g., 'AAPL', 'BTCUSD'
    timeframe: e.g., '1' (1m), '5' (5m), '15' (15m), '60' (1h), 'D' (1 day)
    save_path: where to save the PNG image
    """
    # TradingView uses URL params for symbol, but timeframe is set via UI. We'll default to 1m chart.
    url = f"https://www.tradingview.com/chart/?symbol={symbol}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(6000)  # Wait for chart to load
        # Optionally, interact with the chart to set timeframe (advanced: use selectors)
        page.screenshot(path=save_path, full_page=False)
        browser.close() 