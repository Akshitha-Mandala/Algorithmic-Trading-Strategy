"""
=========================================================
QuantLab - Trading Strategies
=========================================================
"""

import pandas as pd
import vectorbt as vbt


# ==========================================================
# SMA CROSSOVER
# ==========================================================

def sma_crossover(df, fast_window=20, slow_window=50):

    close = df["Close"]

    fast_ma = vbt.MA.run(close, window=fast_window)
    slow_ma = vbt.MA.run(close, window=slow_window)

    entries = fast_ma.ma_crossed_above(slow_ma)
    exits = fast_ma.ma_crossed_below(slow_ma)

    return entries, exits


# ==========================================================
# RSI MEAN REVERSION
# ==========================================================

def rsi_strategy(df,
                 window=14,
                 oversold=30,
                 overbought=70):

    close = df["Close"]

    rsi = vbt.RSI.run(close, window=window)

    entries = rsi.rsi < oversold
    exits = rsi.rsi > overbought

    return entries, exits


# ==========================================================
# MACD
# ==========================================================

def macd_strategy(df,
                  fast=12,
                  slow=26,
                  signal=9):

    close = df["Close"]

    macd = vbt.MACD.run(
        close,
        fast_window=fast,
        slow_window=slow,
        signal_window=signal
    )

    entries = macd.macd_crossed_above(macd.signal)
    exits = macd.macd_crossed_below(macd.signal)

    return entries, exits


# ==========================================================
# MOMENTUM
# ==========================================================

def momentum_strategy(df,
                      lookback=20):

    close = df["Close"]

    momentum = close.pct_change(lookback)

    entries = momentum > 0

    exits = momentum < 0

    return entries, exits


# ==========================================================
# BOLLINGER BANDS
# ==========================================================

def bollinger_strategy(df,
                       window=20,
                       std=2):

    close = df["Close"]

    bb = vbt.BBANDS.run(
        close,
        window=window,
        alpha=std
    )

    entries = close < bb.lower

    exits = close > bb.upper

    return entries, exits


# ==========================================================
# DONCHIAN BREAKOUT
# ==========================================================

def donchian_strategy(df,
                      window=20):

    close = df["Close"]

    upper = df["High"].rolling(window).max()

    lower = df["Low"].rolling(window).min()

    entries = close > upper.shift(1)

    exits = close < lower.shift(1)

    return entries, exits


# ==========================================================
# STRATEGY MAPPING
# ==========================================================

STRATEGIES = {

    "SMA Crossover": sma_crossover,

    "RSI Mean Reversion": rsi_strategy,

    "MACD": macd_strategy,

    "Momentum": momentum_strategy,

    "Bollinger Bands": bollinger_strategy,

    "Donchian Breakout": donchian_strategy

}


# ==========================================================
# RUN STRATEGY
# ==========================================================

def run_strategy(name, df, **kwargs):

    if name not in STRATEGIES:
        raise ValueError(f"Unknown strategy: {name}")

    return STRATEGIES[name](df, **kwargs)