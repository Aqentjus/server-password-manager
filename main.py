import socket

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

# Initialize a variable to store received texts
received_texts = []

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
            received_texts.append(text_to_send)
            print(f"Received and stored: {text_to_send}")
        elif data == '/receive':
            response = '\n'.join(received_texts)
            client_socket.send(response.encode('utf-8'))
        elif data == '/quit':
            break  # Exit the inner loop

    # Close the client socket
    client_socket.close()
