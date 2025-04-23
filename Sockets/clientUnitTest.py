import pytest
from unittest.mock import patch, MagicMock
from stockClient import main, connect_to_server

# Test case for main() function
def test_main():
    # Mock the connect_to_server function to return a mock socket
    with patch('stockClient.connect_to_server', return_value=MagicMock()) as mock_connect:
        # Mock the behavior of the socket's recv method to return a welcome message
        mock_socket = MagicMock()
        mock_socket.recv.return_value = b"Welcome to PriceQuake!"

        # Assign the mock socket to connect_to_server return value
        mock_connect.return_value = mock_socket

        # Use patch to mock the input() function to simulate user input
        with patch('builtins.input', return_value='exit'):
            # Run the main function
            with patch('stockClient.print') as mock_print:  # Mock print to check output
                main()

                # Check that the connection is established and the welcome message is received
                mock_connect.assert_called_once()
                mock_socket.recv.assert_called_once_with(1024)
                mock_print.assert_any_call("Welcome to PriceQuake!")  # Verifying that the welcome message is printed

                # Check that the socket is closed after the main loop ends
                mock_socket.close.assert_called_once()
