import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Stock Chart",
    layout="wide"
)

st.title("📈 Yahoo Finance Stock Chart")

# ---------------- Sidebar ---------------- #

ticker = st.sidebar.text_input(
    "Ticker",
    "AAPL"
).upper()

period = st.sidebar.selectbox(
    "Period",
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

intervals = {
    "1mo": "1d",
    "3mo": "1d",
    "6mo": "1d",
    "1y": "1d",
    "2y": "1wk",
    "5y": "1wk",
    "10y": "1mo",
    "max": "1mo"
}

interval = intervals[period]

# ---------------- Download ---------------- #

try:
    data = yf.download(
        tickers=ticker,
        period=period,
        interval=interval,
        auto_adjust=True,
        progress=False,
        group_by="column"
    )

except Exception as e:
    st.error(f"Download failed.\n\n{e}")
    st.stop()

if data.empty:
    st.error("No data available.")
    st.stop()

# ---------------- Fix MultiIndex ---------------- #

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

required = ["Open", "High", "Low", "Close", "Volume"]

for col in required:
    if col not in data.columns:
        st.error(f"{col} not found.")
        st.stop()

# ---------------- Metrics ---------------- #

close = data["Close"].dropna()

if close.empty:
    st.error("No closing prices available.")
    st.stop()

latest = close.iloc[-1]
first = close.iloc[0]

change = latest - first
pct = (change / first) * 100

c1, c2, c3 = st.columns(3)

c1.metric("Latest Price", f"${latest:.2f}")
c2.metric("Change", f"{change:.2f}")
c3.metric("% Change", f"{pct:.2f}%")

# ---------------- Chart ---------------- #

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=data.index,
        y=close,
        mode="lines",
        name="Close"
    )
)

fig.update_layout(
    template="plotly_white",
    height=600,
    xaxis_title="Date",
    yaxis_title="Price",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- Table ---------------- #

st.subheader("Historical Data")

display_df = data[required].copy()

st.dataframe(display_df, use_container_width=True)
