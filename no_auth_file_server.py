import http.server
import socketserver
import os
import socket

# Define the directory you want to serve
directory_to_serve = './'  # replace with your directory

os.chdir(directory_to_serve)

Handler = http.server.SimpleHTTPRequestHandler

# Get the current system's IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))  # we use the Google's public DNS server to find out our IP
ip_address = s.getsockname()[0]
s.close()

with socketserver.TCPServer((ip_address, 8000), Handler) as httpd:
    print(f"Serving at {ip_address} on port 8000")
    httpd.serve_forever()
