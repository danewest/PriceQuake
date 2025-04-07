import socket
import threading
import psycopg2

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
    client_socket.sendall(b"Welcome to Stock Notifier!\n")