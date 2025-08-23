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

# Global variable to store latest NeoPixel status
latest_neopixel_status = {
    "status": "Unknown",
    "count": 0,
    "board": "Metro M4 Airlift Lite",
    "ip_address": "Unknown",
    "timestamp": 0
}

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            # Return a nice HTML page with NeoPixel status
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Metro M4 Airlift Lite - NeoPixel Status</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }}
        .status-card {{
            background: #f8f9fa;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
        }}
        .status-on {{
            border-color: #28a745;
            background: #d4edda;
        }}
        .status-off {{
            border-color: #6c757d;
            background: #e9ecef;
        }}
        .status-indicator {{
            font-size: 48px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .status-on .status-indicator {{
            color: #28a745;
        }}
        .status-off .status-indicator {{
            color: #6c757d;
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        .info-item {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }}
        .info-label {{
            font-weight: bold;
            color: #495057;
            margin-bottom: 5px;
        }}
        .info-value {{
            color: #212529;
        }}
        .refresh-info {{
            text-align: center;
            color: #6c757d;
            font-size: 14px;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Metro M4 Airlift Lite - NeoPixel Status</h1>
        
        <div class="status-card {'status-on' if latest_neopixel_status['status'] == 'ON' else 'status-off'}">
            <div class="status-indicator">
                {'💡 ON' if latest_neopixel_status['status'] == 'ON' else '⚫ OFF'}
            </div>
            <h2>NeoPixel Status: {latest_neopixel_status['status']}</h2>
        </div>
        
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">Blink Count</div>
                <div class="info-value">{latest_neopixel_status['count']}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Board</div>
                <div class="info-value">{latest_neopixel_status['board']}</div>
            </div>
            <div class="info-item">
                <div class="info-label">IP Address</div>
                <div class="info-value">{latest_neopixel_status['ip_address']}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Last Update</div>
                <div class="info-value">{datetime.fromtimestamp(latest_neopixel_status['timestamp']).strftime('%H:%M:%S') if latest_neopixel_status['timestamp'] > 0 else 'Never'}</div>
            </div>
        </div>
        
        <div class="refresh-info">
            <p>🔄 Refresh this page to see the latest status</p>
            <p>📡 NeoPixel blinks every 4 seconds and sends status updates</p>
        </div>
    </div>
    
    <script>
        // Auto-refresh every 3 seconds
        setTimeout(function() {{
            location.reload();
        }}, 3000);
    </script>
</body>
</html>
            """
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(html_content.encode())
            
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
                
        elif self.path == '/status':
            # Handle NeoPixel status updates
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                print(f"NeoPixel Status: {data}")
                
                # Store the latest status for the web page
                global latest_neopixel_status
                latest_neopixel_status = data
                
                response = {
                    "message": "Status received",
                    "status": data,
                    "timestamp": datetime.now().isoformat()
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                self.wfile.write(json.dumps(response, indent=2).encode())
                
            except Exception as e:
                print(f"Error processing status: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'500 - Internal Server Error')
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

