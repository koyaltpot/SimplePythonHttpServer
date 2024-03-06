import os
import http.server
import socketserver
from http import HTTPStatus
from base64 import b64decode
import socket

# Define your desired username and password
USERNAME = "myuser"
PASSWORD = "mypassword"

class AuthHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Get the Authorization header
        auth_header = self.headers.get("Authorization")

        if auth_header:
            # Extract the base64-encoded credentials
            encoded_credentials = auth_header.split(" ")[-1]
            decoded_credentials = b64decode(encoded_credentials).decode("utf-8")
            username, password = decoded_credentials.split(":")

            # Check if credentials match
            if username == USERNAME and password == PASSWORD:
                return super().do_GET()
            else:
                self.send_response(HTTPStatus.UNAUTHORIZED)
                self.send_header("WWW-Authenticate", 'Basic realm="Secure Area"')
                self.end_headers()
                self.wfile.write(b"Authentication required")
        else:
            self.send_response(HTTPStatus.UNAUTHORIZED)
            self.send_header("WWW-Authenticate", 'Basic realm="Secure Area"')
            self.end_headers()
            self.wfile.write(b"Authentication required")

if __name__ == "__main__":
    PORT = 8000
    DIRECTORY = "./"  # Specify your directory here

    # Change the current working directory
    os.chdir(DIRECTORY)

    # Get the current system's IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  # we use the Google's public DNS server to find out our IP
    ip_address = s.getsockname()[0]
    s.close()

    with socketserver.TCPServer((ip_address, PORT), AuthHTTPRequestHandler) as httpd:
        print(f"Serving at {ip_address} on port {PORT}...")
        httpd.serve_forever()

