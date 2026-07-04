import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Stock Price Dashboard",
    layout="wide"
)

st.title("📈 Stock Price Dashboard (Yahoo Finance)")

# -----------------------------
# Sidebar
# -----------------------------
ticker = st.sidebar.text_input(
    "Enter Stock Symbol",
    value="AAPL"
).upper()

period = st.sidebar.selectbox(
    "Select Time Period",
    [
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y",
        "max"
    ]
)

interval_map = {
    "1mo": "1d",
    "3mo": "1d",
    "6mo": "1d",
    "1y": "1d",
    "2y": "1wk",
    "5y": "1wk",
    "10y": "1mo",
    "max": "1mo"
}

interval = interval_map[period]

# -----------------------------
# Download Data
# -----------------------------
data = yf.download(
    ticker,
    period=period,
    interval=interval,
    auto_adjust=True,
    progress=False
)

if data.empty:
    st.error("No data found.")
    st.stop()

# -----------------------------
# Metrics
# -----------------------------
latest = float(data["Close"].iloc[-1])
first = float(data["Close"].iloc[0])

change = latest - first
pct = change / first * 100

col1, col2, col3 = st.columns(3)

col1.metric("Latest Price", f"${latest:.2f}")
col2.metric("Change", f"{change:.2f}")
col3.metric("% Change", f"{pct:.2f}%")

# -----------------------------
# Line Chart
# -----------------------------
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data["Close"],
        mode="lines",
        name="Close Price"
    )
)

fig.update_layout(
    title=f"{ticker} Closing Price",
    xaxis_title="Date",
    yaxis_title="Price",
    template="plotly_white",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Data Table
# -----------------------------
st.subheader("Historical Data")

st.dataframe(
    data[["Open", "High", "Low", "Close", "Volume"]],
    use_container_width=True
)
