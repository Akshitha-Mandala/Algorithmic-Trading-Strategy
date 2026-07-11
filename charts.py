"""
=========================================================
QuantLab - Charts Module
=========================================================
Interactive Plotly charts for the dashboard.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ==========================================================
# CANDLESTICK CHART
# ==========================================================

def candlestick_chart(data, entries=None, exits=None):

    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="Price"
        )
    )

    # Buy Signals
    if entries is not None:

        buy_price = data.loc[entries, "Close"]

        fig.add_trace(
            go.Scatter(
                x=buy_price.index,
                y=buy_price.values,
                mode="markers",
                marker=dict(
                    symbol="triangle-up",
                    size=12,
                    color="green"
                ),
                name="Buy"
            )
        )

    # Sell Signals
    if exits is not None:

        sell_price = data.loc[exits, "Close"]

        fig.add_trace(
            go.Scatter(
                x=sell_price.index,
                y=sell_price.values,
                mode="markers",
                marker=dict(
                    symbol="triangle-down",
                    size=12,
                    color="red"
                ),
                name="Sell"
            )
        )

    fig.update_layout(
        title="Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        height=650,
        template="plotly_dark"
    )

    return fig


# ==========================================================
# EQUITY CURVE
# ==========================================================

def equity_curve_chart(equity):

    fig = px.line(
        x=equity.index,
        y=equity.values,
        title="Portfolio Equity Curve"
    )

    fig.update_traces(line_width=3)

    fig.update_layout(
        template="plotly_dark",
        height=450,
        xaxis_title="Date",
        yaxis_title="Portfolio Value"
    )

    return fig


# ==========================================================
# BUY & HOLD VS STRATEGY
# ==========================================================

def comparison_chart(strategy_equity, buy_hold_equity):

    df = pd.DataFrame({
        "Strategy": strategy_equity,
        "Buy & Hold": buy_hold_equity
    })

    fig = px.line(
        df,
        title="Strategy vs Buy & Hold"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        xaxis_title="Date",
        yaxis_title="Portfolio Value"
    )

    return fig


# ==========================================================
# DRAWDOWN
# ==========================================================

def drawdown_chart(drawdown):

    fig = px.area(
        x=drawdown.index,
        y=drawdown.values * 100,
        title="Portfolio Drawdown (%)"
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        xaxis_title="Date",
        yaxis_title="Drawdown (%)"
    )

    return fig


# ==========================================================
# MONTHLY RETURNS HEATMAP
# ==========================================================

def monthly_returns_heatmap(monthly_returns):

    df = monthly_returns.to_frame("Return")

    df["Year"] = df.index.year
    df["Month"] = df.index.strftime("%b")

    pivot = df.pivot(
        index="Year",
        columns="Month",
        values="Return"
    )

    month_order = [
        "Jan","Feb","Mar","Apr","May","Jun",
        "Jul","Aug","Sep","Oct","Nov","Dec"
    ]

    pivot = pivot.reindex(columns=month_order)

    fig = px.imshow(
        pivot,
        text_auto=".1f",
        aspect="auto",
        color_continuous_scale="RdYlGn",
        title="Monthly Returns (%)"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    return fig


# ==========================================================
# ROLLING SHARPE
# ==========================================================

def rolling_sharpe_chart(returns, window=60):

    rolling = (
        returns.rolling(window).mean()
        /
        returns.rolling(window).std()
    ) * (252 ** 0.5)

    fig = px.line(
        x=rolling.index,
        y=rolling.values,
        title=f"Rolling Sharpe Ratio ({window} Days)"
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        xaxis_title="Date",
        yaxis_title="Sharpe Ratio"
    )

    return fig


# ==========================================================
# RETURNS DISTRIBUTION
# ==========================================================

def returns_distribution(returns):

    fig = px.histogram(
        returns,
        nbins=50,
        title="Daily Returns Distribution"
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        xaxis_title="Daily Return",
        yaxis_title="Frequency"
    )

    return fig