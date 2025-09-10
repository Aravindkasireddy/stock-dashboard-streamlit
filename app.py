import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import requests

# --------------------------------
# CONFIG
# --------------------------------
ALPHA_VANTAGE_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your Alpha Vantage key

st.set_page_config(page_title="Stock Price Dashboard", layout="wide")
st.title("📈 Stock Price Dashboard")

# --------------------------------
# Sidebar Widgets
# --------------------------------
st.sidebar.header("Stock Selection")

ticker = st.sidebar.text_input(
    "Enter Stock Ticker (e.g. AAPL, TSLA, MSFT):",
    "AAPL"  # default
)

start_date = st.sidebar.date_input(
    "Start Date", 
    pd.to_datetime("2023-01-01")
)

end_date = st.sidebar.date_input(
    "End Date", 
    pd.to_datetime("today")
)

# --------------------------------
# Yahoo Finance (cached)
# --------------------------------
@st.cache_data(ttl=3600)
def load_yf_data(ticker, start, end):
    try:
        return yf.download(ticker, start=start, end=end)
    except Exception as e:
        st.warning(f"Yahoo Finance error: {e}")
        return pd.DataFrame()

# --------------------------------
# Alpha Vantage Fallback (cached)
# --------------------------------
@st.cache_data(ttl=3600)
def load_alpha_vantage(ticker, start, end):
    url = (
        f"https://www.alphavantage.co/query"
        f"?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}"
        f"&apikey={ALPHA_VANTAGE_API_KEY}&outputsize=full"
    )
    try:
        r = requests.get(url)
        data = r.json()

        if "Note" in data:
            st.warning("⏳ Alpha Vantage API limit reached (5 calls/min, 500/day). Please try again later.")
            return pd.DataFrame()
        if "Error Message" in data:
            st.error("❌ Invalid ticker symbol for Alpha Vantage.")
            return pd.DataFrame()
        if "Time Series (Daily)" not in data:
            st.error("❌ No data returned from Alpha Vantage.")
            return pd.DataFrame()

        df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
        df = df.rename(
            columns={
                "1. open": "Open",
                "2. high": "High",
                "3. low": "Low",
                "4. close": "Close",
                "6. volume": "Volume",
            }
        )
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        df = df.astype(float)

        # Filter by chosen date range
        df = df[(df.index >= pd.to_datetime(start)) & (df.index <= pd.to_datetime(end))]
        return df

    except Exception as e:
        st.error(f"Alpha Vantage error: {e}")
        return pd.DataFrame()

# --------------------------------
# Main Logic
# --------------------------------
if ticker:
    df = load_yf_data(ticker, start_date, end_date)

    # Fallback to Alpha Vantage
    if df.empty:
        st.info("⚠️ Yahoo Finance rate-limited. Switching to Alpha Vantage...")
        df = load_alpha_vantage(ticker, start_date, end_date)

    if not df.empty:
        st.subheader(f"{ticker} Stock Data")

        # ✅ Reset index so "Date" appears as a column
        df_display = df.reset_index()
        st.dataframe(df_display.tail())

        # Plot Closing Price
        st.subheader("Closing Price Trend")
        fig, ax = plt.subplots()
        ax.plot(df.index, df["Close"], label="Close Price", color="blue")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")
        ax.legend()
        st.pyplot(fig)

        # Download CSV
        st.download_button(
            label="📥 Download CSV",
            data=df_display.to_csv(index=False).encode("utf-8"),
            file_name=f"{ticker}_stock_data.csv",
            mime="text/csv",
        )
    else:
        st.warning("No data found for this ticker. Try another symbol.")
