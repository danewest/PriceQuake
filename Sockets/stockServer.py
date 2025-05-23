import socket
import threading
import psycopg2
import sys
import os

# Adding project root to the path to allow for App imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from App.services import stock_fetcher

HOST = '0.0.0.0'
PORT = 5000

# Database connection
#connection = psycopg2.connect(
 #   dbname='stockdb',
  #  user='admin',
   # password='adminpass',
    #host='localhost',
    #port='5432'
#)

# Handles incoming clients
def handle_client(client_socket, address):
    print(f"[+] New connection from {address}")
    # Welcome message
    client_socket.sendall(b"Welcome to PriceQuake!\n")

    try:
        while True:
            data = client_socket.recv(1024).decode().strip()
            # If there is no data or the user requests to exit
            # then the connection ends.
            if not data or data.lower() == 'exit':
                break
            # If a client's message starts with "GET:" it will create a variable
            # with the text after it, then compare that text to the available stocks.
            # If it matches an available one then the price will be fetched. If not
            # it will let the error know that there has been a problem.
            if data.startswith("GET:"):
                symbol = data.split(":", 1)[1].strip().upper()
                result = stock_fetcher.get_stock_price(symbol)

                if "error" in result:
                    response = f"Error: {result['error']}\n"
                else:
                    price = result["price"]
                    response = f"{symbol}'s current price: ${price:.2f}\n"

                client_socket.sendall(response.encode())
            else:
                client_socket.sendall(b"Unknown command.\n")
        print(f"[-] Connection with {address} closed.\n")
        client_socket.close()
    # Error handling
    except ConnectionResetError:
        print(f"[-] Client {address}")

def start_server():
    print(f"[*] Starting server on {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"[*] Listening on {HOST}:{PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()

if __name__ == "__main__":
    start_server()