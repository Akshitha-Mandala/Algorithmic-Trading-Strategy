"""
=========================================================
QuantLab - Utility Functions
=========================================================
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np


# ==========================================================
# DOWNLOAD STOCK DATA
# ==========================================================

@st.cache_data(show_spinner=False)
def download_data(ticker, start_date, end_date):
    """
    Download historical stock data from Yahoo Finance.
    """

    df = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False
    )

    if df.empty:
        raise ValueError(f"No data found for {ticker}")

    # Normalize single-ticker MultiIndex columns from yfinance
    if isinstance(df.columns, pd.MultiIndex):
        if df.columns.nlevels == 2:
            df.columns = df.columns.get_level_values(0)
        else:
            raise ValueError("Unexpected multi-level columns from Yahoo Finance.")

    # Keep only required columns
    columns = ["Open", "High", "Low", "Close", "Volume"]

    df = df[columns]

    df.dropna(inplace=True)

    return df


# ==========================================================
# VALIDATE DATA
# ==========================================================

def validate_data(df):

    if df is None:
        return False

    if df.empty:
        return False

    if len(df) < 50:
        return False

    return True


# ==========================================================
# BUY & HOLD RETURN
# ==========================================================

def buy_and_hold_return(df):

    start_price = df["Close"].iloc[0]

    end_price = df["Close"].iloc[-1]

    return ((end_price - start_price) / start_price) * 100


# ==========================================================
# DAILY RETURNS
# ==========================================================

def _ensure_value_series(series):
    if isinstance(series, pd.DataFrame):
        if series.shape[1] == 1:
            return series.iloc[:, 0]
        raise ValueError(
            "Expected a single Close series but received multiple columns."
        )
    return series


def daily_returns(df):

    close = _ensure_value_series(df["Close"])

    return close.pct_change().dropna()


# ==========================================================
# CUMULATIVE RETURNS
# ==========================================================

def cumulative_returns(df):

    returns = daily_returns(df)

    cumulative = (1 + returns).cumprod()

    return cumulative


# ==========================================================
# LATEST PRICE
# ==========================================================

def latest_price(df):

    close = _ensure_value_series(df["Close"])

    return float(close.iloc[-1])


# ==========================================================
# PRICE CHANGE
# ==========================================================

def latest_change(df):

    close = _ensure_value_series(df["Close"])

    if len(close) < 2:
        raise ValueError("Not enough data to calculate latest price change.")

    change = close.iloc[-1] - close.iloc[-2]

    pct = (change / close.iloc[-2]) * 100

    return float(change), float(pct)


# ==========================================================
# LATEST VOLUME
# ==========================================================

def latest_volume(df):

    volume_series = _ensure_value_series(df["Volume"])

    return int(volume_series.iloc[-1])


# ==========================================================
# FORMAT CURRENCY
# ==========================================================

def format_currency(value):

    return f"{value:,.2f}"


# ==========================================================
# FORMAT PERCENT
# ==========================================================

def format_percent(value):

    return f"{value:.2f}%"


# ==========================================================
# DATA SUMMARY
# ==========================================================

def get_summary(df):

    change, pct = latest_change(df)

    return {

        "Current Price": latest_price(df),

        "Change": change,

        "Change %": pct,

        "Volume": latest_volume(df),

        "Buy & Hold": float(buy_and_hold_return(df))

    }


# ==========================================================
# EXPORT TRADES
# ==========================================================

def export_csv(df):

    return df.to_csv(index=False).encode("utf-8")


# ==========================================================
# DATE RANGE
# ==========================================================

def trading_days(df):

    return len(df)


# ==========================================================
# VOLATILITY
# ==========================================================

def annual_volatility(df):

    returns = daily_returns(df)

    return returns.std() * np.sqrt(252) * 100


# ==========================================================
# CAGR
# ==========================================================

def calculate_cagr(df):

    years = (df.index[-1] - df.index[0]).days / 365.25

    start = df["Close"].iloc[0]

    end = df["Close"].iloc[-1]

    cagr = ((end / start) ** (1 / years) - 1) * 100

    return cagr