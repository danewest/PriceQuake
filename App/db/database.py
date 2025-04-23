# This file is for future use when I apply user functionality and stock history. For the scope of the project this is not needed

import yfinance as yf
import psycopg2
import os

# Connects to the PriceQuake database
def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "stockdb"),
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD", "adminpass,"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )

# Test function to see if pulling information works using Apple stock
def get_apple():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM stocks WHERE symbol = 'AAPL'")
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0] if result else None

# Retrieve price of stock that matches given symbol
def get_stock_price(symbol):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT price FROM stocks WHERE symbol = %s;", (symbol,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0] if result else None

# Adds a new user to the PriceQuake database
def add_user(username, password_hash, email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s);",
                (username, password_hash, email))
    conn.commit()
    cur.close()
    conn.close()
