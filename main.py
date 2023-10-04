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
        if data.startswith('/add '):
            data = data[len('/add '):]
            try:
                new_password = json.loads(data)
            except json.JSONDecodeError:
                print("Invalid JSON format for password data.")
                continue

            # Load existing passwords
            passwords = load_from_json()

            # Add the new password to the existing data
            service = new_password.get('service')
            passwords[service] = new_password
            print(f"Received and stored password for service: {service}")

            # Save the updated data to the JSON file instantly
            save_to_json(passwords)

        elif data == '/get':
            # Load passwords from the JSON file when '/get' is requested
            passwords = load_from_json()
            client_socket.send(json.dumps(passwords).encode('utf-8'))

        elif data.startswith('/get '):
            # Extract the service name from the request
            service_to_find = data[len('/get '):]

            # Load passwords from the JSON file
            passwords = load_from_json()

            # Check if the requested service exists
            if service_to_find in passwords:
                response = json.dumps(passwords[service_to_find])
                client_socket.send(response.encode('utf-8'))
            else:
                client_socket.send("Service not found.".encode('utf-8'))

        elif data == '/quit':
            break  # Exit the inner loop

        else:
            # Handle unknown commands here (e.g., print an error message)
            print(f"Unknown command: {data}")

    # Close the client socket
    client_socket.close()
