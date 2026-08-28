import streamlit as st
import yfinance as yf
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Soros Strategy Hub", layout="wide")
st.title("📈 Soros-Style Market Reflexivity Hub")
st.write("Analyze individual stock psychology or compare multiple assets side-by-side using reflexivity rules.")

# Create Navigation Tabs
tab1, tab2 = st.tabs(["📊 Multi-Stock Comparison Matrix", "🔍 Single Ticker Deep-Dive"])

# -------------------------------------------------------------
# TAB 1: COMPARISON FEATURE
# -------------------------------------------------------------
with tab1:
    st.subheader("Compare Multiple Tickers Side-by-Side")
    # Accept a list of tickers separated by commas
    tickers_input = st.text_input(
        "Enter multiple tickers separated by commas (e.g., AAPL, NVDA, TSLA, MSFT):", 
        value="AAPL, NVDA, TSLA"
    )
    
    # Process the text input into an array of clean tickers
    ticker_list = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    
    if st.button("Generate Comparison Matrix") and ticker_list:
        comparison_data = []
        
        with st.spinner("Processing market matrix..."):
            for ticker_symbol in ticker_list:
                try:
                    ticker = yf.Ticker(ticker_symbol)
                    info = ticker.info
                    history = ticker.history(period="1y")
                    
                    if history.empty or 'trailingPE' not in info:
                        continue
                        
                    # Fetch specs
                    current_price = info.get('currentPrice', history['Close'].iloc[-1])
                    pe_ratio = info.get('trailingPE', 0)
                    debt_to_equity = info.get('debtToEquity', 0)
                    earnings_growth = info.get('earningsGrowth', 0) * 100
                    
                    # Trend rules
                    history['SMA50'] = history['Close'].rolling(window=50).mean()
                    history['SMA200'] = history['Close'].rolling(window=200).mean()
                    is_trending_up = current_price > history['SMA50'].iloc[-1] > history['SMA200'].iloc[-1]
                    
                    # Expectation Gap / Signals
                    expectation_gap = "Normal"
                    if pe_ratio > 45 and earnings_growth < 5:
                        expectation_gap = "Bubble Risk"
                    elif pe_ratio < 15 and earnings_growth > 15:
                        expectation_gap = "Undervalued"
                        
                    if is_trending_up and expectation_gap != "Bubble Risk":
                        signal = "🟢 BUY (Momentum)"
                    elif expectation_gap == "Bubble Risk":
                        signal = "🔴 AVOID (Bubble)"
                    elif debt_to_equity > 150:
                        signal = "🟡 AVOID (High Debt)"
                    else:
                        signal = "⚪ HOLD / NEUTRAL"
                        
                    # Pack rows into array
                    comparison_data.append({
                        "Ticker": ticker_symbol,
                        "Current Price": f"${current_price:.2f}",
                        "P/E Ratio": f"{pe_ratio:.2f}",
                        "Earnings Growth": f"{earnings_growth:.2f}%",
                        "Debt-to-Equity": f"{debt_to_equity:.2f}%",
                        "Trend Status": "Bullish 📈" if is_trending_up else "Bearish/Flat 📉",
                        "Expectation Gap": expectation_gap,
                        "Action Signal": signal
                    })
                except Exception:
                    pass # Ignore faulty symbols smoothly
                    
        if comparison_data:
            df = pd.DataFrame(comparison_data)
            st.dataframe(df.set_index("Ticker"), use_container_width=True)
        else:
            st.error("No valid ticker data could be scraped. Double-check your symbols.")

# -------------------------------------------------------------
# TAB 2: SINGLE TICKER DEEP DIVE
# -------------------------------------------------------------
with tab2:
    st.subheader("Single Stock Core Evaluation")
    single_input = st.text_input("Enter a single ticker for deep trend analytics:", value="AAPL").upper().strip()
    
    if single_input:
        with st.spinner("Loading deep analytical feed..."):
            t = yf.Ticker(single_input)
            inf = t.info
            hist = t.history(period="1y")
            
        if hist.empty or 'trailingPE' not in inf:
            st.error(f"Could not load data for {single_input}")
        else:
            c_price = inf.get('currentPrice', hist['Close'].iloc[-1])
            pe = inf.get('trailingPE', 0)
            d_e = inf.get('debtToEquity', 0)
            eg = inf.get('earningsGrowth', 0) * 100
            
            hist['SMA50'] = hist['Close'].rolling(window=50).mean()
            hist['SMA200'] = hist['Close'].rolling(window=200).mean()
            up_trend = c_price > hist['SMA50'].iloc[-1] > hist['SMA200'].iloc[-1]
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Price", f"${c_price:.2f}")
            col2.metric("P/E Ratio", f"{pe:.2f}")
            col3.metric("YOY Earnings", f"{eg:.2f}%")
            col4.metric("Debt-to-Equity", f"{d_e:.2f}%")
            
            # Simple chart logic
            chart_df = pd.DataFrame({
                'Close Price': hist['Close'],
                '50 SMA': hist['SMA50'],
                '200 SMA': hist['SMA200']
            })
            st.line_chart(chart_df)
