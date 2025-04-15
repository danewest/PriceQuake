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
    client_socket.sendall(b"Welcome to PriceQuake!\n")

    try:
        while True:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break
            if data.startswith("GET:"):
                symbol = data.split(":", 1)[1].strip().upper()
                cursor = connection.cursor()
                cursor.execute("SELECT FROM stocks WHERE symbol = %s", (symbol,))
                result = cursor.fetchone()
                if result:
                    price = result[0]
                    message = f"{symbol}: ${price}\n"
                else:
                    message = f"{symbol} not found in database.\n"
                client_socket.sendall(message.encode())
            else:
                client_socket.sendall(b"Unknown command.\n")

    except ConnectionResetError:
        print(f"[-] Client {address}")

def start_server():
    print(f"[*] Starting server on {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        while True:
            client_socket, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()

if __name__ == "__main__":
    start_server()