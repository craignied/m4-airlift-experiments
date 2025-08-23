#!/usr/bin/env python3
"""
Simple HTTP Server for Metro M4 Airlift Lite WiFi Testing
Run this on your Mac to test WiFi connectivity from the Metro M4
"""

import http.server
import socketserver
import json
from datetime import datetime
import socket

# Configuration
PORT = 8000
HOST = '0.0.0.0'  # Listen on all interfaces

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            # Return a simple JSON response
            response = {
                "message": "Hello from Mac Server!",
                "timestamp": datetime.now().isoformat(),
                "status": "success",
                "board": "Metro M4 Airlift Lite WiFi Test"
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif self.path == '/status':
            # Return server status
            response = {
                "server": "Mac Simple HTTP Server",
                "uptime": "running",
                "timestamp": datetime.now().isoformat()
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        else:
            # Return 404 for unknown paths
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 - Not Found')

    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/data':
            # Get the content length
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Try to parse as JSON
                data = json.loads(post_data.decode('utf-8'))
                print(f"Received data: {data}")
                
                response = {
                    "message": "Data received successfully",
                    "received_data": data,
                    "timestamp": datetime.now().isoformat()
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                self.wfile.write(json.dumps(response, indent=2).encode())
                
            except json.JSONDecodeError:
                # Handle non-JSON data
                response = {
                    "message": "Data received (not JSON)",
                    "received_data": post_data.decode('utf-8'),
                    "timestamp": datetime.now().isoformat()
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                self.wfile.write(json.dumps(response, indent=2).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 - Not Found')

def get_local_ip():
    """Get the local IP address of this Mac"""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

if __name__ == "__main__":
    local_ip = get_local_ip()
    
    print("🚀 Starting Simple HTTP Server for Metro M4 WiFi Testing")
    print(f"📍 Server IP: {local_ip}")
    print(f"🌐 Port: {PORT}")
    print(f"📡 URL: http://{local_ip}:{PORT}")
    print("\n📋 Available endpoints:")
    print(f"   GET  http://{local_ip}:{PORT}/          - Simple JSON response")
    print(f"   GET  http://{local_ip}:{PORT}/status    - Server status")
    print(f"   POST http://{local_ip}:{PORT}/data      - Receive data from Metro M4")
    print("\n⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        with socketserver.TCPServer((HOST, PORT), SimpleHTTPRequestHandler) as httpd:
            print(f"✅ Server started successfully!")
            print(f"🔗 Metro M4 can connect to: http://{local_ip}:{PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

