import socket
import threading
import psycopg2
from database import get_stock_price

HOST = '0.0.0.0'
PORT = 65432

# Database connection
connection = psycopg2.connect(
    dbname='stockdb',
    user='admin',
    password='adminpass',
    host='localhost',
    port='5432'
)

def handle_client(client_socket, address):
    print(f"[+] New connection from {address}")
    client_socket.sendall(b"Welcome to PriceQuake!\n")

    # Example interaction -> Sending stock data

    cursor = connection.cursor()
    cursor.execute("SELECT symbol, price FROM stocks LIMIT 5;")
    for symbol, price in cursor.fetchall():
        message = f"{symbol}: ${price}\n"
        client_socket.sendall(message.encode())

    client_socket.close()

def start_server():
    print(f"[*] Starting server on {HOST}:{PORT}")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()