import yfinance as yf
import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "stockdb"),
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD", "adminpass,"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )

def get_apple():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM stocks WHERE symbol = 'AAPL'")
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0] if result else None

def get_stock_price(symbol):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT price FROM stocks WHERE symbol = %s;", (symbol,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0] if result else None

def add_user(username, password_hash, email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s);",
                (username, password_hash, email))
    conn.commit()
    cur.close()
    conn.close()