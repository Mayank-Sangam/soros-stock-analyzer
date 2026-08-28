# 📈 George Soros-Style Market Reflexivity Hub

An interactive web dashboard built with Python and Streamlit that evaluates global market equities through the lens of George Soros's trading philosophy. It combines real-time technical momentum filters with underlying corporate health metrics to identify market misperceptions and potential "boom-bust" cycles.

Live web app link: *[PASTE YOUR LIVE STREAMLIT LINK HERE]*

## 🚀 Key Features
* **Multi-Stock Comparison Matrix:** Input multiple tickers (e.g., AAPL, NVDA, TSLA) to view a side-by-side comparison of market trends and fundamental valuation gaps.
* **Single Ticker Deep-Dive:** Drill into individual stocks with an interactive 1-year historical chart mapping the price against 50-day and 200-day Simple Moving Averages (SMA).
* **Algorithmic Action Signals:** Generates dynamic `BUY`, `HOLD`, or `AVOID` recommendations based on market psychology and structural risks.

## 🧠 The Strategy Logic
Inspired by George Soros's macro framework, this tool monitors two distinct forces:
1. **Reflexivity (Market Psychology):** Measures the *Expectation Gap* between what the market is paying (P/E Ratio) and what the company is actually generating (YOY Earnings Growth) to identify inflating bubbles.
2. **Trend Momentum:** Employs a dual-moving average crossover system to ensure you only ride the trend when positive reflexivity is actively driving the price upward.
3. **Systemic Risk Filter:** Automatically flags and avoids companies carrying excessive debt loads (Debt-to-Equity > 150%) that make them highly vulnerable during market corrections.

## 🛠️ Built With
* **Python 3** - Core system logic
* **Streamlit** - Web application and dashboard framework
* **Yahoo Finance API (`yfinance`)** - Real-time market database engine
* **Pandas** - Data structuring and matrix computation
