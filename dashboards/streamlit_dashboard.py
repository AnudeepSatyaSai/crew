import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

def widget_ticker_tape():
    components.html("""
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
      {
      "symbols": [
        { "proName": "FOREXCOM:SPXUSD", "title": "S&P 500" },
        { "proName": "FOREXCOM:NSXUSD", "title": "US 100" },
        { "proName": "FX_IDC:EURUSD", "title": "EUR/USD" },
        { "proName": "BITSTAMP:BTCUSD", "title": "Bitcoin" },
        { "proName": "BITSTAMP:ETHUSD", "title": "Ethereum" }
      ],
      "showSymbolLogo": true,
      "colorTheme": "light",
      "isTransparent": false,
      "displayMode": "adaptive",
      "locale": "en"
    }
      </script>
    </div>
    <!-- TradingView Widget END -->
    """, height=75)

def widget_advanced_chart(symbol, interval):
    components.html(f"""
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div id="tradingview_{symbol}"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "width": "100%",
        "height": 500,
        "symbol": "{symbol}",
        "interval": "{interval}",
        "timezone": "Etc/UTC",
        "theme": "light",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_{symbol}"
      }});
      </script>
    </div>
    <!-- TradingView Widget END -->
    """, height=520)

def widget_symbol_overview(symbol):
    components.html(f"""
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-overview.js" async>
      {{
      "symbols": [ [ "{symbol}|1D" ] ],
      "chartOnly": false,
      "width": "100%",
      "height": 400,
      "locale": "en",
      "colorTheme": "light",
      "autosize": true,
      "showVolume": false,
      "showMA": false,
      "hideDateRanges": false,
      "hideMarketStatus": false,
      "hideSymbolLogo": false,
      "scalePosition": "right",
      "scaleMode": "Normal",
      "fontFamily": "-apple-system, BlinkMacSystemFont, Trebuchet MS, Roboto, Ubuntu, sans-serif",
      "fontSize": "10",
      "noTimeScale": false,
      "valuesTracking": "1",
      "changeMode": "price-and-percent",
      "chartType": "area",
      "maLineColor": "#2962FF",
      "maLineWidth": 1,
      "maLength": 9,
      "lineWidth": 2,
      "lineType": 0,
      "dateRanges": [ "1d|1", "1w|15", "1m|30", "3m|60", "12m|1D", "60m|1W", "all|1M" ]
    }}
      </script>
    </div>
    <!-- TradingView Widget END -->
    """, height=400)

def widget_technical_analysis(symbol):
    components.html(f"""
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
      {{
      "interval": "1D",
      "width": "100%",
      "isTransparent": false,
      "height": 400,
      "symbol": "{symbol}",
      "showIntervalTabs": true,
      "locale": "en",
      "colorTheme": "light"
    }}
      </script>
    </div>
    <!-- TradingView Widget END -->
    """, height=400)

def widget_company_profile(symbol):
    components.html(f"""
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-profile.js" async>
      {{
      "symbol": "{symbol}",
      "width": "100%",
      "height": 500,
      "colorTheme": "light",
      "isTransparent": false,
      "locale": "en"
    }}
      </script>
    </div>
    <!-- TradingView Widget END -->
    """, height=500)

def widget_market_overview():
    components.html("""
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-market-overview.js" async>
      {
      "colorTheme": "light",
      "dateRange": "12M",
      "showChart": true,
      "locale": "en",
      "largeChartUrl": "",
      "isTransparent": false,
      "showSymbolLogo": true,
      "showFloatingTooltip": false,
      "width": "100%",
      "height": 600,
      "plotLineColorGrowing": "rgba(41, 98, 255, 1)",
      "plotLineColorFalling": "rgba(41, 98, 255, 1)",
      "gridLineColor": "rgba(240, 243, 250, 0)",
      "scaleFontColor": "rgba(120, 123, 134, 1)",
      "belowLineFillColorGrowing": "rgba(41, 98, 255, 0.12)",
      "belowLineFillColorFalling": "rgba(41, 98, 255, 0.12)",
      "belowLineFillColorGrowingBottom": "rgba(41, 98, 255, 0)",
      "belowLineFillColorFallingBottom": "rgba(41, 98, 255, 0)",
      "symbolActiveColor": "rgba(41, 98, 255, 0.12)",
      "tabs": [
        {
          "title": "Indices",
          "symbols": [ { "s": "FOREXCOM:SPXUSD" }, { "s": "FOREXCOM:NSXUSD" }, { "s": "FOREXCOM:DJI" } ],
          "originalTitle": "Indices"
        },
        {
          "title": "Futures",
          "symbols": [ { "s": "CME_MINI:ES1!" }, { "s": "CME:6E1!" }, { "s": "COMEX:GC1!" } ],
          "originalTitle": "Futures"
        },
        {
          "title": "Bonds",
          "symbols": [ { "s": "CME:GE1!" }, { "s": "CBOT:ZB1!" }, { "s": "CBOT:UB1!" } ],
          "originalTitle": "Bonds"
        },
        {
          "title": "Forex",
          "symbols": [ { "s": "FX:EURUSD" }, { "s": "FX:GBPUSD" }, { "s": "FX:USDJPY" } ],
          "originalTitle": "Forex"
        }
      ]
    }
      </script>
    </div>
    <!-- TradingView Widget END -->
    """, height=600)

def widget_economic_calendar():
    components.html("""
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>
      {
      "colorTheme": "light",
      "isTransparent": false,
      "width": "100%",
      "height": 600,
      "locale": "en",
      "importanceFilter": "-1,0,1"
    }
      </script>
    </div>
    <!-- TradingView Widget END -->
    """, height=600)

def widget_top_stories(symbol):
    components.html(f"""
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-timeline.js" async>
      {{
      "feedMode": "symbol",
      "symbol": "{symbol}",
      "isTransparent": false,
      "displayMode": "regular",
      "width": "100%",
      "height": 500,
      "colorTheme": "light",
      "locale": "en"
    }}
      </script>
    </div>
    <!-- TradingView Widget END -->
    """, height=500)

def main():
    st.set_page_config(layout="wide")
    st.title('Trading Analysis Dashboard')

    widget_ticker_tape()

    # Sidebar for symbol and interval selection
    st.sidebar.title("Controls")
    symbol = st.sidebar.text_input('Symbol (e.g., AAPL, BTCUSD):', 'AAPL')
    interval = st.sidebar.selectbox('Timeframe:', ['1', '5', '15', '60', 'D', 'W', 'M'], index=4)

    # Main dashboard with tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Live Chart & Signals", "Symbol Details", "Market Pulse", "Custom Analysis"])

    with tab1:
        st.header(f"Live Chart for {symbol}")
        widget_advanced_chart(symbol, interval)

    with tab2:
        st.header(f"Details for {symbol}")
        col1, col2 = st.columns(2)
        with col1:
            widget_symbol_overview(symbol)
            widget_company_profile(symbol)
        with col2:
            widget_technical_analysis(symbol)
            widget_top_stories(symbol)

    with tab3:
        st.header("Market Pulse")
        col1, col2 = st.columns(2)
        with col1:
            widget_market_overview()
        with col2:
            widget_economic_calendar()

    with tab4:
        st.header("Custom Analysis from Your Pipeline")
        # Upload and display signals
        uploaded_file = st.file_uploader('Upload Signals CSV', type='csv')
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.write(df.head())
            if 'ensemble_signal' in df.columns:
                st.line_chart(df['ensemble_signal'])
                # Show alerts for signals
                alerts = df[df['ensemble_signal'] != 0]
                for idx, row in alerts.iterrows():
                    st.warning(f"ALERT: Signal {row['ensemble_signal']} at index {idx}")

            if 'llm_summary' in df.columns:
                st.write('LLM Explanations:')
                st.write(df['llm_summary'].head())

if __name__ == '__main__':
    main() 