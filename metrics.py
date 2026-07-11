import pandas as pd

def performance_summary(portfolio):

    stats = {

        "Total Return (%)":
            round(portfolio.total_return()*100,2),

        "Buy & Hold Return (%)":
            round(
                (
                    portfolio.close.iloc[-1] /
                    portfolio.close.iloc[0]
                    -1
                )*100,
                2
            ),

        "Annual Return (%)":
            round(portfolio.annualized_return()*100,2),

        "Sharpe Ratio":
            round(portfolio.sharpe_ratio(),2),

        "Sortino Ratio":
            round(portfolio.sortino_ratio(),2),

        "Calmar Ratio":
            round(portfolio.calmar_ratio(),2),

        "Max Drawdown (%)":
            round(portfolio.max_drawdown()*100,2),

        "Volatility (%)":
            round(portfolio.annualized_volatility()*100,2),

        "Win Rate (%)":
            round(portfolio.trades.win_rate()*100,2),

        "Total Trades":
            int(portfolio.trades.count())

    }

    return pd.DataFrame(
        stats.items(),
        columns=["Metric","Value"]
    )