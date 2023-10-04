from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Define a handler for incoming requests
class PasswordManagerHandler(BaseHTTPRequestHandler):
    passwords = []

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())

        # Store 'data' in the passwords list (you should handle this securely)
        self.passwords.append(data)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Password added successfully.')

    def do_GET(self):
        if self.path == '/passwords':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Send the passwords as JSON to the client
            self.wfile.write(json.dumps(self.passwords).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

# Create an HTTP server to handle incoming requests
server_address = ('', 8080)
httpd = HTTPServer(server_address, PasswordManagerHandler)
print('Server running on port 8080...')
httpd.serve_forever()
