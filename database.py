"""
=========================================================
QuantLab - Database Module
=========================================================
Handles SQLite database operations.
"""

import sqlite3
import pandas as pd
from pathlib import Path

# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(exist_ok=True)

# The stock CSV file is stored in the repository under database/data
DATA_DIR = DATABASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATABASE_DIR / "stocks.db"

CSV_PATH = DATA_DIR / "stocks.csv"


# ==========================================================
# CONNECTION
# ==========================================================

def get_connection():

    return sqlite3.connect(DB_PATH)


# ==========================================================
# CREATE TABLES
# ==========================================================

def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    # ---------------- Stocks ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stocks(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        ticker TEXT UNIQUE NOT NULL,

        market TEXT NOT NULL,

        sector TEXT NOT NULL

    )
    """)

    # ---------------- Backtest History ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS backtest_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        run_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        stock TEXT,

        strategy TEXT,

        total_return REAL,

        buy_hold_return REAL,

        sharpe REAL,

        sortino REAL,

        max_drawdown REAL,

        cagr REAL,

        volatility REAL,

        win_rate REAL

    )
    """)

    # ---------------- Trade History ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trade_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        stock TEXT,

        strategy TEXT,

        trade_date TEXT,

        action TEXT,

        price REAL,

        quantity INTEGER,

        pnl REAL

    )
    """)

    conn.commit()

    conn.close()


# ==========================================================
# LOAD STOCKS FROM CSV
# ==========================================================

def load_stocks():

    if not CSV_PATH.exists():

        raise FileNotFoundError(

            f"stocks.csv not found:\n{CSV_PATH}"

        )

    stocks = pd.read_csv(CSV_PATH)

    conn = get_connection()

    stocks.to_sql(

        "stocks",

        conn,

        if_exists="replace",

        index=False

    )

    conn.close()


# ==========================================================
# GET ALL STOCKS
# ==========================================================

def get_all_stocks():

    conn = get_connection()

    df = pd.read_sql(

        "SELECT * FROM stocks ORDER BY name",

        conn

    )

    conn.close()

    return df


# ==========================================================
# GET MARKETS
# ==========================================================

def get_markets():

    conn = get_connection()

    df = pd.read_sql("""

        SELECT DISTINCT market

        FROM stocks

        ORDER BY market

    """, conn)

    conn.close()

    return df["market"].tolist()


# ==========================================================
# GET SECTORS
# ==========================================================

def get_sectors(market):

    conn = get_connection()

    df = pd.read_sql("""

        SELECT DISTINCT sector

        FROM stocks

        WHERE market=?

        ORDER BY sector

    """,

    conn,

    params=[market]

    )

    conn.close()

    return df["sector"].tolist()


# ==========================================================
# GET STOCKS BY FILTER
# ==========================================================

def get_stocks(

        market=None,

        sector=None

):

    conn = get_connection()

    query = "SELECT * FROM stocks"

    params = []

    conditions = []

    if market:

        conditions.append("market=?")

        params.append(market)

    if sector:

        conditions.append("sector=?")

        params.append(sector)

    if conditions:

        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY name"

    df = pd.read_sql(

        query,

        conn,

        params=params

    )

    conn.close()

    return df


# ==========================================================
# SAVE BACKTEST
# ==========================================================

def save_backtest(

        stock,

        strategy,

        total_return,

        buy_hold,

        sharpe,

        sortino,

        mdd,

        cagr,

        volatility,

        win_rate

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO backtest_history(

        stock,

        strategy,

        total_return,

        buy_hold_return,

        sharpe,

        sortino,

        max_drawdown,

        cagr,

        volatility,

        win_rate

    )

    VALUES (?,?,?,?,?,?,?,?,?,?)

    """,

    (

        stock,

        strategy,

        total_return,

        buy_hold,

        sharpe,

        sortino,

        mdd,

        cagr,

        volatility,

        win_rate

    )

    )

    conn.commit()

    conn.close()


# ==========================================================
# SAVE TRADE HISTORY
# ==========================================================

def save_trade_history(trades):

    if trades.empty:

        return

    conn = get_connection()

    trades.to_sql(

        "trade_history",

        conn,

        if_exists="append",

        index=False

    )

    conn.close()


# ==========================================================
# GET BACKTEST HISTORY
# ==========================================================

def get_backtest_history():

    conn = get_connection()

    df = pd.read_sql("""

        SELECT *

        FROM backtest_history

        ORDER BY run_date DESC

    """,

    conn)

    conn.close()

    return df


# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

def initialize_database():

    create_tables()

    load_stocks()


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    initialize_database()

    print("================================")

    print("Database Created Successfully")

    print(f"Database : {DB_PATH}")

    print()

    print(get_all_stocks().head())

    print()

    print("Total Stocks :", len(get_all_stocks()))

    print("================================")