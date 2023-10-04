import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server's host and port
server_host = '192.168.1.116'  # Replace with the Raspberry Pi's IP address
server_port = 12345                      # Use the same port as in the server

# Connect to the server
client_socket.connect((server_host, server_port))

while True:
    # Get user input
    user_input = input("Enter a command: ")

    # Send the user input to the server
    client_socket.send(user_input.encode('utf-8'))

    # Receive and print the server's response
    response = client_socket.recv(1024).decode('utf-8')
    print(response)

# Close the client socket when done

client_socket.close()
