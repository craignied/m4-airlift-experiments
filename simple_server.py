#!/usr/bin/env python3
"""
Real-time WebSocket Server for Metro M4 Airlift Lite
Run this on your Mac for real-time sensor data display
"""

import asyncio
import websockets
import json
from datetime import datetime
import threading
import time
import http.server
import socketserver
import socket

# Configuration
WS_PORT = 8765  # WebSocket port
HTTP_PORT = 8000  # HTTP port for the web page
HOST = '0.0.0.0'  # Listen on all interfaces

# Global variables
latest_neopixel_status = {
    "status": "Unknown",
    "count": 0,
    "board": "Metro M4 Airlift Lite",
    "ip_address": "Unknown",
    "timestamp": 0
}

# WebSocket connections
websocket_clients = set()

# Queue for broadcasting updates
broadcast_queue = asyncio.Queue()

# Thread-safe status update mechanism
status_update_queue = []
status_update_lock = threading.Lock()

# WebSocket handler
async def websocket_handler(websocket):
    """Handle WebSocket connections for real-time updates"""
    print(f"🔌 New WebSocket connection from {websocket.remote_address}")
    websocket_clients.add(websocket)
    
    try:
        # Send current status immediately
        await websocket.send(json.dumps(latest_neopixel_status))
        print(f"✅ Sent initial status to {websocket.remote_address}")
        
        # Keep connection alive with proper message handling
        async for message in websocket:
            try:
                # Handle ping/pong for connection health
                if message == "ping":
                    await websocket.send("pong")
                    print(f"🏓 Ping-pong with {websocket.remote_address}")
                else:
                    # Handle any other messages from client
                    print(f"📨 Received message from {websocket.remote_address}: {message}")
            except Exception as e:
                print(f"⚠️ Error handling message from {websocket.remote_address}: {e}")
                break
                
    except websockets.exceptions.ConnectionClosed:
        print(f"🔌 WebSocket connection closed from {websocket.remote_address}")
    except Exception as e:
        print(f"❌ WebSocket error with {websocket.remote_address}: {e}")
    finally:
        websocket_clients.discard(websocket)
        print(f"🔌 Removed WebSocket client {websocket.remote_address}")

async def broadcast_status():
    """Broadcast status updates to all WebSocket clients"""
    if websocket_clients:
        message = json.dumps(latest_neopixel_status)
        await asyncio.gather(
            *[client.send(message) for client in websocket_clients],
            return_exceptions=True
        )

def update_status_and_broadcast(new_status):
    """Update status and queue broadcast to all WebSocket clients"""
    global latest_neopixel_status
    latest_neopixel_status = new_status
    
    # Use thread-safe queue for status updates
    with status_update_lock:
        status_update_queue.append(new_status)
        print(f"📡 Added status update to queue: {new_status.get('status', 'unknown')} (count: {new_status.get('count', 'unknown')})")

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
            <h1>🚀 Metro M4 Airlift Lite - Real-time Status</h1>
            
            <div class="status-card {'status-on' if latest_neopixel_status['status'] == 'ON' else 'status-off'}">
                <div class="status-indicator">
                    {'💡 ON' if latest_neopixel_status['status'] == 'ON' else '⚫ OFF'}
                </div>
                <h2>NeoPixel Status: {latest_neopixel_status['status']}</h2>
            </div>
            
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Blink Count</div>
                    <div class="info-value" id="blink-count">{latest_neopixel_status['count']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Board</div>
                    <div class="info-value" id="board-name">{latest_neopixel_status['board']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">IP Address</div>
                    <div class="info-value" id="ip-address">{latest_neopixel_status['ip_address']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Last Update</div>
                    <div class="info-value" id="last-update">{datetime.fromtimestamp(latest_neopixel_status['timestamp']).strftime('%H:%M:%S') if latest_neopixel_status['timestamp'] > 0 else 'Never'}</div>
                </div>
            </div>
            
            <div class="refresh-info">
                <p>🔌 WebSocket Status: <span id="connection-status">🟡 Connecting...</span></p>
                <p>⚡ Real-time updates via WebSocket connection</p>
                <p>📡 NeoPixel blinks every 4 seconds and sends instant updates</p>
            </div>
    </div>
    
            <script>
            // Real-time WebSocket connection with automatic reconnection
            let ws = null;
            let reconnectAttempts = 0;
            const maxReconnectAttempts = 5;
            
            function connectWebSocket() {{
                ws = new WebSocket('ws://192.168.1.192:8765');
                
                ws.onopen = function() {{
                    console.log('WebSocket connected');
                    document.getElementById('connection-status').textContent = '🟢 Connected';
                    reconnectAttempts = 0; // Reset reconnect attempts on successful connection
                    
                    // Start ping interval to keep connection alive
                    if (ws.pingInterval) {{
                        clearInterval(ws.pingInterval);
                    }}
                    ws.pingInterval = setInterval(function() {{
                        if (ws.readyState === WebSocket.OPEN) {{
                            ws.send('ping');
                        }}
                    }}, 30000); // Ping every 30 seconds
                }};
                
                ws.onmessage = function(event) {{
                    console.log('Received WebSocket message:', event.data);
                    try {{
                        const data = JSON.parse(event.data);
                        updateDisplay(data);
                    }} catch (error) {{
                        console.error('Error parsing WebSocket message:', error);
                    }}
                }};
                
                ws.onclose = function() {{
                    console.log('WebSocket disconnected');
                    document.getElementById('connection-status').textContent = '🟡 Reconnecting...';
                    
                    // Clear ping interval
                    if (ws.pingInterval) {{
                        clearInterval(ws.pingInterval);
                        ws.pingInterval = null;
                    }}
                    
                    // Try to reconnect instead of reloading the page
                    if (reconnectAttempts < maxReconnectAttempts) {{
                        reconnectAttempts++;
                        console.log('Reconnect attempt ' + reconnectAttempts + '/' + maxReconnectAttempts);
                        setTimeout(connectWebSocket, 2000);
                    }} else {{
                        document.getElementById('connection-status').textContent = '🔴 Connection failed';
                        console.log('Max reconnect attempts reached');
                    }}
                }};
                
                ws.onerror = function(error) {{
                    console.error('WebSocket error:', error);
                    document.getElementById('connection-status').textContent = '🔴 Error';
                }};
            }}
            
            function updateDisplay(data) {{
                console.log('Updating display with data:', data);
                
                // Update status card
                const statusCard = document.querySelector('.status-card');
                const statusIndicator = document.querySelector('.status-indicator');
                const statusText = document.querySelector('h2');
                
                if (data.status === 'ON') {{
                    statusCard.className = 'status-card status-on';
                    statusIndicator.textContent = '💡 ON';
                    statusText.textContent = 'NeoPixel Status: ON';
                }} else {{
                    statusCard.className = 'status-card status-off';
                    statusIndicator.textContent = '⚫ OFF';
                    statusText.textContent = 'NeoPixel Status: OFF';
                }}
                
                // Update info grid
                document.getElementById('blink-count').textContent = data.count;
                document.getElementById('board-name').textContent = data.board;
                document.getElementById('ip-address').textContent = data.ip_address;
                
                const timestamp = new Date(data.timestamp * 1000);
                document.getElementById('last-update').textContent = timestamp.toLocaleTimeString();
                
                console.log('Display updated successfully');
            }}
            
            // Start the WebSocket connection
            connectWebSocket();
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
                
                # Update status and broadcast to all WebSocket clients
                update_status_and_broadcast(data)
                
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

async def broadcast_processor():
    """Background task to process broadcast queue"""
    print("🔄 Broadcast processor started")
    while True:
        try:
            # Check for new status updates from the thread-safe queue
            updates_to_process = []
            with status_update_lock:
                if status_update_queue:
                    updates_to_process = status_update_queue.copy()
                    status_update_queue.clear()
            
            # Process any updates
            for new_status in updates_to_process:
                print(f"📥 Processing broadcast: {new_status.get('status', 'unknown')} (count: {new_status.get('count', 'unknown')})")
                
                # Broadcast to all connected WebSocket clients
                if websocket_clients:
                    message = json.dumps(new_status)
                    results = await asyncio.gather(
                        *[client.send(message) for client in websocket_clients],
                        return_exceptions=True
                    )
                    
                    # Check for any errors
                    errors = [r for r in results if isinstance(r, Exception)]
                    if errors:
                        print(f"⚠️ Some clients failed to receive broadcast: {errors}")
                    else:
                        print(f"✅ Successfully broadcasted to {len(websocket_clients)} clients")
                else:
                    print("⚠️ No WebSocket clients connected")
            
            # Small delay to prevent busy waiting
            await asyncio.sleep(0.1)
            
        except Exception as e:
            print(f"❌ Error in broadcast processor: {e}")
            await asyncio.sleep(1)

async def main():
    """Main function to run both HTTP and WebSocket servers"""
    local_ip = get_local_ip()
    print(f"🚀 Starting Real-time WebSocket Server for Metro M4")
    print(f"📍 Server IP: {local_ip}")
    print(f"🌐 HTTP Port: {HTTP_PORT}")
    print(f"🔌 WebSocket Port: {WS_PORT}")
    print(f"📡 HTTP URL: http://{local_ip}:{HTTP_PORT}")
    print(f"🔌 WebSocket URL: ws://{local_ip}:{WS_PORT}")
    print(f"📋 Available endpoints:")
    print(f"   GET  http://{local_ip}:{HTTP_PORT}/          - Real-time web interface")
    print(f"   POST http://{local_ip}:{HTTP_PORT}/status    - Receive status from Metro M4")
    print(f"   POST http://{local_ip}:{HTTP_PORT}/data      - Receive data from Metro M4")
    print(f"⏹️  Press Ctrl+C to stop the server")
    print(f"--------------------------------------------------")
    
    # Start HTTP server in a separate thread
    def run_http_server():
        with socketserver.TCPServer((HOST, HTTP_PORT), SimpleHTTPRequestHandler) as httpd:
            print(f"✅ HTTP Server started on port {HTTP_PORT}")
            httpd.serve_forever()
    
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()
    
    # Start WebSocket server and broadcast processor
    print(f"✅ WebSocket Server starting on port {WS_PORT}")
    async with websockets.serve(websocket_handler, HOST, WS_PORT):
        print(f"🔌 WebSocket Server ready for real-time connections")
        print(f"🔗 Metro M4 can connect to: http://{local_ip}:{HTTP_PORT}")
        
        # Start the broadcast processor task
        broadcast_task = asyncio.create_task(broadcast_processor())
        
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

