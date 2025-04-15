import socket

HOST = '127.0.0.1' # Change this to Debian server IP when testing cross-device
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    welcome = s.recv(1024).decode()
    print(welcome)

    while True:
        cmd = input("Enter command (GET:<symbol> or 'exit'): ").strip()
        if cmd.lower() == 'exit':
            break

        s.sendall(cmd.encode())
        response = s.recv(1024).decode()
        print(response)