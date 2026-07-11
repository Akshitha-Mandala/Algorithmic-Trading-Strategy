"""
=========================================================
QuantLab - Algorithmic Trading Platform
=========================================================
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
from datetime import date

# Project Modules
import con_fig
from database import (
    initialize_database,
    get_markets,
    get_sectors,
    get_stocks
)

from utils import (
    download_data,
    validate_data,
    get_summary,
    format_currency,
    format_percent
)

from strategies import run_strategy

from backtest import (
    run_backtest,
    backtest_summary,
    buy_and_hold_equity
)

from metrics import performance_summary

from charts import (
    candlestick_chart,
    equity_curve_chart,
    comparison_chart,
    drawdown_chart,
    monthly_returns_heatmap,
    rolling_sharpe_chart,
    returns_distribution
)

# --------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------

st.set_page_config(
    page_title=con_fig.APP_TITLE,
    page_icon=con_fig.PAGE_ICON,
    layout=con_fig.LAYOUT
)

st.title(con_fig.APP_TITLE)

st.caption("Professional Quantitative Trading & Backtesting Platform")

# --------------------------------------------------------
# DATABASE
# --------------------------------------------------------

try:
    initialize_database()
except Exception as e:
    st.error(e)
    st.stop()

# --------------------------------------------------------
# SIDEBAR
# --------------------------------------------------------

st.sidebar.title("Backtest Settings")

# Market

markets = get_markets()

market = st.sidebar.selectbox(
    "Market",
    markets
)

# Sector

sectors = get_sectors(market)

sector = st.sidebar.selectbox(
    "Sector",
    sectors
)

# Stocks

stocks = get_stocks(
    market=market,
    sector=sector
)

stock_name = st.sidebar.selectbox(
    "Stock",
    stocks["name"]
)

ticker = stocks.loc[
    stocks["name"] == stock_name,
    "ticker"
].iloc[0]

# --------------------------------------------------------
# STRATEGY
# --------------------------------------------------------

strategy = st.sidebar.selectbox(
    "Strategy",
    con_fig.STRATEGIES
)

# --------------------------------------------------------
# DATES
# --------------------------------------------------------

start_date = st.sidebar.date_input(
    "Start Date",
    pd.to_datetime(con_fig.DEFAULT_START_DATE)
)

end_date = st.sidebar.date_input(
    "End Date",
    date.today()
)

# --------------------------------------------------------
# CAPITAL
# --------------------------------------------------------

capital = st.sidebar.number_input(
    "Initial Capital",
    min_value=10000,
    value=con_fig.DEFAULT_CAPITAL,
    step=10000
)

fees = st.sidebar.number_input(
    "Commission",
    value=con_fig.DEFAULT_COMMISSION,
    format="%.4f"
)

slippage = st.sidebar.number_input(
    "Slippage",
    value=con_fig.DEFAULT_SLIPPAGE,
    format="%.4f"
)

# --------------------------------------------------------
# RUN BUTTON
# --------------------------------------------------------

run = st.sidebar.button(
    "Run Backtest",
    use_container_width=True
)

# --------------------------------------------------------
# MAIN
# --------------------------------------------------------

if not run:

    st.info("Select your settings from the sidebar and click **Run Backtest**.")

    st.stop()

# --------------------------------------------------------
# DOWNLOAD DATA
# --------------------------------------------------------

with st.spinner("Downloading market data..."):

    data = download_data(
        ticker,
        start_date,
        end_date
    )

if not validate_data(data):

    st.error("Not enough historical data.")

    st.stop()

# --------------------------------------------------------
# STOCK SUMMARY
# --------------------------------------------------------

summary = get_summary(data)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Current Price",
    format_currency(summary["Current Price"])
)

col2.metric(
    "Change %",
    format_percent(summary["Change %"])
)

col3.metric(
    "Volume",
    f"{summary['Volume']:,}"
)

col4.metric(
    "Buy & Hold",
    format_percent(summary["Buy & Hold"])
)

st.divider()

# --------------------------------------------------------
# RUN STRATEGY
# --------------------------------------------------------

with st.spinner("Generating trading signals..."):

    try:

        entries, exits = run_strategy(
            strategy,
            data
        )

    except Exception as e:

        st.error(f"Strategy Error:\n{e}")

        st.stop()

# --------------------------------------------------------
# RUN BACKTEST
# --------------------------------------------------------

with st.spinner("Running Backtest..."):

    portfolio = run_backtest(

        price=data["Close"],

        entries=entries,

        exits=exits,

        initial_cash=capital,

        fees=fees,

        slippage=slippage

    )

# --------------------------------------------------------
# BACKTEST SUMMARY
# --------------------------------------------------------

results = backtest_summary(portfolio)

equity = results["equity_curve"]

returns = results["returns"]

drawdown = results["drawdown"]

monthly = results["monthly_returns"]

yearly = results["yearly_returns"]

trades = results["trade_history"]

# --------------------------------------------------------
# BUY & HOLD
# --------------------------------------------------------

buy_hold = buy_and_hold_equity(

    data["Close"],

    capital

)

# --------------------------------------------------------
# PERFORMANCE METRICS
# --------------------------------------------------------

metrics = performance_summary(portfolio)

# --------------------------------------------------------
# DISPLAY METRICS
# --------------------------------------------------------

st.subheader("Performance Summary")

metric_dict = dict(

    zip(

        metrics["Metric"],

        metrics["Value"]

    )

)

c1, c2, c3, c4 = st.columns(4)

c1.metric(

    "Total Return",

    f"{metric_dict['Total Return (%)']}%"

)

c2.metric(

    "Sharpe Ratio",

    metric_dict["Sharpe Ratio"]

)

c3.metric(

    "Max Drawdown",

    f"{metric_dict['Max Drawdown (%)']}%"

)

c4.metric(

    "Win Rate",

    f"{metric_dict['Win Rate (%)']}%"

)

st.dataframe(

    metrics,

    use_container_width=True,

    hide_index=True

)

st.divider()


# ==========================================================
# CHARTS
# ==========================================================

st.header("📊 Performance Charts")

# ----------------------------------------------------------
# Candlestick Chart
# ----------------------------------------------------------

st.subheader("Candlestick Chart")

fig = candlestick_chart(
    data,
    entries,
    exits
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------------
# Equity Curve
# ----------------------------------------------------------

st.subheader("Portfolio Equity Curve")

fig = equity_curve_chart(
    equity
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------------
# Strategy vs Buy & Hold
# ----------------------------------------------------------

st.subheader("Strategy vs Buy & Hold")

fig = comparison_chart(
    equity,
    buy_hold
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------------
# Drawdown
# ----------------------------------------------------------

st.subheader("Drawdown")

fig = drawdown_chart(
    drawdown
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------------
# Monthly Returns Heatmap
# ----------------------------------------------------------

st.subheader("Monthly Returns Heatmap")

fig = monthly_returns_heatmap(
    monthly
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------------
# Rolling Sharpe Ratio
# ----------------------------------------------------------

st.subheader("Rolling Sharpe Ratio")

fig = rolling_sharpe_chart(
    returns
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------------
# Returns Distribution
# ----------------------------------------------------------

st.subheader("Daily Returns Distribution")

fig = returns_distribution(
    returns
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==========================================================
# TRADE HISTORY
# ==========================================================

st.header("📑 Trade History")

if trades.empty:

    st.info("No trades were executed for the selected strategy.")

else:

    st.dataframe(
        trades,
        use_container_width=True,
        hide_index=True
    )

# ==========================================================
# DOWNLOAD TRADE HISTORY
# ==========================================================

if not trades.empty:

    csv = trades.to_csv(index=False).encode("utf-8")

    st.download_button(

        label="⬇ Download Trade History",

        data=csv,

        file_name="trade_history.csv",

        mime="text/csv"

    )

# ==========================================================
# SAVE BACKTEST TO DATABASE
# ==========================================================

try:

    from database import save_backtest

    save_backtest(

        stock=stock_name,

        strategy=strategy,

        total_return=float(metric_dict["Total Return (%)"]),

        buy_hold=float(summary["Buy & Hold"]),

        sharpe=float(metric_dict["Sharpe Ratio"]),

        sortino=float(metric_dict["Sortino Ratio"]),

        mdd=float(metric_dict["Max Drawdown (%)"]),

        cagr=float(metric_dict["Annual Return (%)"]),

        volatility=float(metric_dict["Volatility (%)"]),

        win_rate=float(metric_dict["Win Rate (%)"])

    )

except Exception:

    pass

# ==========================================================
# BACKTEST HISTORY
# ==========================================================

st.header("📚 Previous Backtests")

try:

    from database import get_backtest_history

    history = get_backtest_history()

    if not history.empty:

        st.dataframe(

            history,

            use_container_width=True,

            hide_index=True

        )

    else:

        st.info("No previous backtests available.")

except Exception:

    st.info("Backtest history unavailable.")

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.markdown(
"""
---
### 📈 QuantLab – Algorithmic Trading Platform

**Features**

- Multiple Trading Strategies
- Portfolio Backtesting
- Buy & Hold Comparison
- Performance Metrics
- Interactive Plotly Charts
- SQLite Database
- Trade History
- CSV Export

Developed using:

- Streamlit
- VectorBT
- Plotly
- Pandas
- SQLite
- Yahoo Finance (yfinance)

© 2026 QuantLab
"""
)