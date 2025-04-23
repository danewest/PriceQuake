import socket
import time

#from pydantic_core.core_schema import none_schema

HOST = '127.0.0.1' # Change this to Debian server IP when testing cross-device
PORT = 5000

# Connects to the server, throws errors if fails
def connect_to_server():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        return s
    except ConnectionRefusedError:
        print("Connection failed: The server may be unavailable.")
        return None
    except Exception as e:
        print(f"Unexpected error during connection to the server: {e}")
        return None

# Main function for client functionality
def main():
    s = connect_to_server()

    # Tries reconnecting to the server every 5 seconds until either it succeeds or user cancels
    if s is None:
        print("Unable to connect to the server. Retrying every 5 seconds... Press CTRL+C to exit PriceQuake.")
        while s is None:
            time.sleep(5)
            s = connect_to_server()

    # Connects to the server to receive welcome message
    try:
        welcome = s.recv(1024).decode()
        print(welcome)
    except Exception as e:
        print(f"Failed to receive welcome message from the server: {e}")
        s.close()
        return

    # Prompt user on how to use program
    print("Enter command ('GET:{Insert symbol here!}' or 'exit'): \n")
    print("For any questions about how to work PriceQuake please refer to the README!\n")
    while True:
        cmd = input("> ").strip()
        # Ends process
        if cmd.lower() == 'exit':
            break
        # Sends user response, exceptions for if it fails
        try:
            s.sendall(cmd.encode())
            response = s.recv(1024).decode()
            print(response)
        # If the response cannot be sent/cannot reach location these exceptions occur
        except (ConnectionResetError, BrokenPipeError):
            print("Connection lost. Trying to reconnect...")
            s.close()
            s = None
            while s is None:
                s = connect_to_server()
                if s:
                    # Reconnection try and catch
                    try:
                        welcome = s.recv(1024).decode()
                        print(welcome)
                    except Exception as e:
                        print(f"Error after reconnect: {e}")
                        s.close()
                        s = None
                else:
                    print("Still waiting...")
                    time.sleep(5)
        # Unknown error occurs if there is a problem that isn't one of the two above
        except Exception as e:
            print(f"Unexpected error while trying to connect: {e}")
            continue
    if s:
        s.close()

if __name__ == "__main__":
    main()