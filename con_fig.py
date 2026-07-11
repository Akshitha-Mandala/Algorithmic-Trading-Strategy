"""
==========================================================
QuantLab - Algorithmic Trading Platform
Configuration File
==========================================================
"""

# ==========================================================
# APP SETTINGS
# ==========================================================

APP_TITLE = "📈 QuantLab - Algorithmic Trading Platform"

PAGE_ICON = "📊"

LAYOUT = "wide"


# ==========================================================
# DEFAULT BACKTEST SETTINGS
# ==========================================================

DEFAULT_CAPITAL = 100000

DEFAULT_COMMISSION = 0.001      # 0.10%

DEFAULT_SLIPPAGE = 0.0005        # 0.05%

DEFAULT_RISK_FREE_RATE = 0.05    # 5%

DEFAULT_START_DATE = "2018-01-01"


# ==========================================================
# STRATEGIES
# ==========================================================

STRATEGIES = [
    "SMA Crossover",
    "RSI Mean Reversion",
    "MACD",
    "Momentum",
    "Bollinger Bands",
    "Donchian Breakout"
]


# ==========================================================
# DEFAULT STRATEGY PARAMETERS
# ==========================================================

SMA_FAST = 20
SMA_SLOW = 50

RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

MOMENTUM_PERIOD = 20

BOLLINGER_PERIOD = 20
BOLLINGER_STD = 2

DONCHIAN_PERIOD = 20


# ==========================================================
# MARKETS
# ==========================================================

MARKETS = [
    "India",
    "USA"
]


# ==========================================================
# INDIAN STOCKS
# ==========================================================

INDIAN_STOCKS = {

    "Reliance Industries": "RELIANCE.NS",

    "TCS": "TCS.NS",

    "Infosys": "INFY.NS",

    "HDFC Bank": "HDFCBANK.NS",

    "ICICI Bank": "ICICIBANK.NS",

    "State Bank of India": "SBIN.NS",

    "Axis Bank": "AXISBANK.NS",

    "Kotak Mahindra Bank": "KOTAKBANK.NS",

    "Bank of Baroda": "BANKBARODA.NS",

    "Canara Bank": "CANBK.NS",

    "Punjab National Bank": "PNB.NS",

    "Federal Bank": "FEDERALBNK.NS",

    "IndusInd Bank": "INDUSINDBK.NS",

    "IDFC First Bank": "IDFCFIRSTB.NS",

    "AU Small Finance Bank": "AUBANK.NS",

    "ITC": "ITC.NS",

    "Bharti Airtel": "BHARTIARTL.NS",

    "Larsen & Toubro": "LT.NS",

    "Asian Paints": "ASIANPAINT.NS",

    "Wipro": "WIPRO.NS",

    "Tata Motors": "TATAMOTORS.NS",

    "Maruti Suzuki": "MARUTI.NS",

    "Sun Pharma": "SUNPHARMA.NS",

    "UltraTech Cement": "ULTRACEMCO.NS"
}


# ==========================================================
# US STOCKS
# ==========================================================

US_STOCKS = {

    "Apple": "AAPL",

    "Microsoft": "MSFT",

    "Amazon": "AMZN",

    "Google": "GOOGL",

    "Tesla": "TSLA",

    "Meta": "META",

    "NVIDIA": "NVDA",

    "Netflix": "NFLX",

    "AMD": "AMD",

    "Intel": "INTC",

    "Broadcom": "AVGO",

    "Oracle": "ORCL",

    "JPMorgan Chase": "JPM",

    "Goldman Sachs": "GS",

    "Morgan Stanley": "MS",

    "Bank of America": "BAC",

    "Wells Fargo": "WFC",

    "Visa": "V",

    "Mastercard": "MA",

    "Coca-Cola": "KO",

    "PepsiCo": "PEP",

    "Nike": "NKE",

    "Disney": "DIS",

    "Pfizer": "PFE"
}


# ==========================================================
# SECTORS
# ==========================================================

SECTORS = [

    "All",

    "Banking",

    "Technology",

    "Automobile",

    "Healthcare",

    "FMCG"

]


# ==========================================================
# CHART SETTINGS
# ==========================================================

CHART_HEIGHT = 650

THEME = "plotly_dark"

SHOW_RANGESLIDER = False


# ==========================================================
# COLORS
# ==========================================================

BUY_COLOR = "green"

SELL_COLOR = "red"

EQUITY_COLOR = "cyan"

DRAWDOWN_COLOR = "orange"

BUY_HOLD_COLOR = "royalblue"

STRATEGY_COLOR = "gold"


# ==========================================================
# FILE NAMES
# ==========================================================

CSV_FILE = "trade_history.csv"

PDF_FILE = "performance_report.pdf"