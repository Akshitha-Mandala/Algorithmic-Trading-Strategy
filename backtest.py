"""
=========================================================
QuantLab - Backtesting Engine
=========================================================
Handles portfolio creation and backtest-related utilities.
"""

import pandas as pd
import vectorbt as vbt


# ==========================================================
# RUN BACKTEST
# ==========================================================

def run_backtest(
    price,
    entries,
    exits,
    initial_cash=100000,
    fees=0.001,
    slippage=0.0005
):
    """
    Create and run a VectorBT portfolio using entry/exit signals.
    """

    portfolio = vbt.Portfolio.from_signals(
        close=price,
        entries=entries,
        exits=exits,
        init_cash=initial_cash,
        fees=fees,
        slippage=slippage,
        freq="1D"
    )

    return portfolio


# ==========================================================
# EQUITY CURVE
# ==========================================================

def equity_curve(portfolio):
    """
    Portfolio value over time.
    """
    return portfolio.value()


# ==========================================================
# DAILY RETURNS
# ==========================================================

def daily_returns(portfolio):
    """
    Daily portfolio returns.
    """
    return portfolio.returns()


# ==========================================================
# DRAWDOWN CURVE
# ==========================================================

def drawdown_curve(portfolio):
    """
    Portfolio drawdown over time.
    """
    return portfolio.drawdown()


# ==========================================================
# TRADE HISTORY
# ==========================================================

def trade_history(portfolio):
    """
    Returns readable trade history.
    """

    try:
        return portfolio.trades.records_readable

    except Exception:
        return pd.DataFrame()


# ==========================================================
# MONTHLY RETURNS
# ==========================================================

def monthly_returns(portfolio):
    """
    Monthly compounded returns (%).
    """

    returns = portfolio.returns()

    monthly = (
        returns
        .resample("ME")
        .apply(lambda x: (1 + x).prod() - 1)
    )

    return monthly * 100


# ==========================================================
# YEARLY RETURNS
# ==========================================================

def yearly_returns(portfolio):
    """
    Yearly compounded returns (%).
    """

    returns = portfolio.returns()

    yearly = (
        returns
        .resample("YE")
        .apply(lambda x: (1 + x).prod() - 1)
    )

    return yearly * 100


# ==========================================================
# BUY & HOLD EQUITY
# ==========================================================

def buy_and_hold_equity(price, initial_cash=100000):
    """
    Calculate Buy & Hold equity curve.
    """

    normalized = price / price.iloc[0]

    equity = normalized * initial_cash

    return equity


# ==========================================================
# EXPORT TRADE HISTORY
# ==========================================================

def export_trade_history(portfolio):
    """
    Export trade history as CSV bytes.
    """

    trades = trade_history(portfolio)

    if trades.empty:
        return None

    return trades.to_csv(index=False).encode("utf-8")


# ==========================================================
# BACKTEST SUMMARY
# ==========================================================

def backtest_summary(portfolio):
    """
    Returns important portfolio objects for the dashboard.
    """

    return {
        "portfolio": portfolio,
        "equity_curve": equity_curve(portfolio),
        "returns": daily_returns(portfolio),
        "drawdown": drawdown_curve(portfolio),
        "monthly_returns": monthly_returns(portfolio),
        "yearly_returns": yearly_returns(portfolio),
        "trade_history": trade_history(portfolio)
    }