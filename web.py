import socket
import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

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
json_file_path = 'passwords.json'

# Function to save passwords to a JSON file
def save_passwords(passwords):
    with open(json_file_path, 'w') as json_file:
        json.dump(passwords, json_file)

# Function to load passwords from a JSON file
def load_passwords():
    if os.path.exists(json_file_path):
        try:
            with open(json_file_path, 'r') as json_file:
                return json.load(json_file)
        except json.JSONDecodeError:
            return {}
    else:
        return {}

@app.route('/add', methods=['POST'])
def add_password():
    try:
        data = request.json
        # Process and store the password data as before
        # Load existing passwords
        passwords = load_passwords()
        # Add the new password to the existing data
        service = data.get('service')
        passwords[service] = data
        print(f"Received and stored password for service: {service}")
        # Save the updated data to the JSON file instantly
        save_passwords(passwords)
        return "Password added successfully."
    except Exception as e:
        return str(e), 400

@app.route('/get', methods=['POST'])
def get_password():
    try:
        service_to_find = request.data.decode('utf-8')
        # Retrieve and return the password for the specified service
        # Load passwords from the JSON file
        passwords = load_passwords()
        # Check if the requested service exists
        if service_to_find in passwords:
            response = jsonify(passwords[service_to_find])
            return response
        else:
            return "Service not found.", 404
    except Exception as e:
        return str(e), 400

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
            passwords = load_passwords()

            # Add the new password to the existing data
            service = new_password.get('service')
            passwords[service] = new_password
            print(f"Received and stored password for service: {service}")

            # Save the updated data to the JSON file instantly
            save_passwords(passwords)

        elif data.startswith('/get '):
            # Extract the service name from the request
            service_to_find = data[len('/get '):]

            # Load passwords from the JSON file
            passwords = load_passwords()

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Change port as needed for your web interface
