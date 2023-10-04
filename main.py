import socket
import threading
import json
import os

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host and port for the server
host = '0.0.0.0'  # Listen on all available network interfaces
port = 12345     # You can choose any available port

# Bind the socket to the host and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(5)

print(f"Server is listening on {host}:{port}")

# JSON file path
json_file_path = 'received_texts.json'

# Function to save received texts to a JSON file
def save_to_json(received_texts):
    with open(json_file_path, 'w') as json_file:
        json.dump(received_texts, json_file)

# Function to load received texts from a JSON file
def load_from_json():
    if os.path.exists(json_file_path):
        try:
            with open(json_file_path, 'r') as json_file:
                return json.load(json_file)
        except json.JSONDecodeError:
            return []
    else:
        return []

while True:
    # Accept a client connection
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr} has been established.")

    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')

        # Process the received data
        if data.startswith('/send '):
            text_to_send = data[len('/send '):]

            # Load received texts from the JSON file
            received_texts = load_from_json()

            # Append the new text to the existing data
            received_texts.append(text_to_send)
            print(f"Received and stored: {text_to_send}")

            # Save the updated data to the JSON file instantly
            save_to_json(received_texts)
        elif data == '/receive':
            # Load received texts from the JSON file when '/receive' is requested
            received_texts = load_from_json()
            response = '\n'.join(received_texts)
            client_socket.send(response.encode('utf-8'))
        elif data == '/quit':
            break  # Exit the inner loop
        else:
            # Handle unknown commands here (e.g., print an error message)
            print(f"Unknown command: {data}")

    # Close the client socket
    client_socket.close()
