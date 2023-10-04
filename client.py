import socket
import json

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server's host and port
server_host = '192.168.1.116'  # Replace with the Raspberry Pi's IP address
server_port = 12345            # Use the same port as in the server

# Connect to the server
client_socket.connect((server_host, server_port))

while True:
    print("1. Add a new password")
    print("2. Get a password")
    print("/quit")
    choice = input("> ")

    if choice == "1":
        service = input("Enter service name: ")
        username = input("Enter username: ")
        password = input("Enter password: ")

        password_data = {
            "service": service,
            "username": username,
            "password": password
        }

        user_input = "/add " + json.dumps(password_data)
        client_socket.send(user_input.encode('utf-8'))

        print("Password added successfully.")

    elif choice == "2":
        service_to_find = input("Enter service name to retrieve password: ")
        user_input = "/get " + service_to_find
        client_socket.send(user_input.encode('utf-8'))

        response = client_socket.recv(1024).decode('utf-8')
        print(response)

    elif choice == "/quit":
        client_socket.send(choice.encode('utf-8'))
        break

    else:
        print("Invalid command!")

# Close the client socket when done
client_socket.close()
