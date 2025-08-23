# WiFi Proof of Concept Setup Guide

This guide will help you set up a WiFi proof of concept between your Metro M4 Airlift Lite and your Mac.

## 🖥️ Mac Server Setup

### 1. Start the Simple HTTP Server

The `simple_server.py` file creates a simple HTTP server on your Mac for testing WiFi connectivity.

```bash
# Make sure you're in the project directory
cd /Users/craign/code/CircuitPython/MetroM4Airlift

# Start the server
python3 simple_server.py
```

**Expected Output:**
```
🚀 Starting Simple HTTP Server for Metro M4 WiFi Testing
📍 Server IP: 192.168.1.148
🌐 Port: 8000
📡 URL: http://192.168.1.148:8000

📋 Available endpoints:
   GET  http://192.168.1.148:8000/          - Simple JSON response
   GET  http://192.168.1.148:8000/status    - Server status
   POST http://192.168.1.148:8000/data      - Receive data from Metro M4

⏹️  Press Ctrl+C to stop the server
--------------------------------------------------
✅ Server started successfully!
🔗 Metro M4 can connect to: http://192.168.1.148:8000
```

### 2. Test the Server

Open a new terminal and test the server:

```bash
# Test the root endpoint
curl http://192.168.1.148:8000/

# Test the status endpoint
curl http://192.168.1.148:8000/status
```

## 🔧 Metro M4 Setup

### 1. Required Libraries

Make sure these libraries are in `/Volumes/CIRCUITPY/lib/`:
- `adafruit_esp32spi/` (WiFi co-processor)
- `adafruit_requests.mpy` (HTTP requests)
- `neopixel.mpy` (LED control)

### 2. Configure WiFi Credentials

Edit `config.py` with your actual WiFi credentials:

```python
WIFI_SSID = "YOUR_ACTUAL_WIFI_NAME"
WIFI_PASSWORD = "YOUR_ACTUAL_WIFI_PASSWORD"
SERVER_IP = "192.168.1.148"  # Update if your Mac has a different IP
```

### 3. Verify Server IP

Make sure the server IP matches your Mac's IP address:

```python
# Server Configuration
SERVER_IP = "192.168.1.148"  # Update if your Mac has a different IP
```

### 4. Upload and Run

```bash
# Copy the program to the Metro M4
cp wifi_proof_of_concept.py /Volumes/CIRCUITPY/code.py
```

## 🚀 Running the Proof of Concept

### 1. Start the Mac Server
```bash
python3 simple_server.py
```

### 2. Upload and Run on Metro M4
The program will automatically run when uploaded as `code.py`.

### 3. Watch the NeoPixel Status

- **Yellow**: Connecting to WiFi
- **Green**: WiFi connected
- **Blue**: Testing server connection
- **Purple**: Sending data to server
- **Red**: Error occurred
- **Off**: Test complete

### 4. Monitor Output

Watch the CircuitPython serial output for detailed status messages.

## 📡 Expected Results

### Successful Run:
```
🚀 Metro M4 Airlift Lite - WiFi Proof of Concept
==================================================
📡 Target Server: http://192.168.1.148:8000
🔧 ESP32 SPI initialized

🎯 Starting WiFi Proof of Concept...
💡 Connecting to WiFi...
📶 Connecting to: YOUR_WIFI_SSID
⏳ Waiting for WiFi connection...
✅ Connected to WiFi: YOUR_WIFI_SSID
🌐 IP Address: 192.168.1.xxx
💡 WiFi Connected!
💡 Testing server connection...
🔗 Testing GET request to: http://192.168.1.148:8000/
✅ Server responded successfully!
📄 Response: {"message": "Hello from Mac Server!", ...}
💡 Server connection successful!
💡 Sending data to server...
📤 Sending data to: http://192.168.1.148:8000/data
📦 Data: {'board': 'Metro M4 Airlift Lite', ...}
✅ Data sent successfully!
💡 Data sent successfully!

🎉 WiFi Proof of Concept completed successfully!
💡 All tests passed!
```

### Mac Server Output:
```
Received data: {'board': 'Metro M4 Airlift Lite', 'message': 'Hello from CircuitPython!', 'timestamp': 1234567890.123, 'neopixel_status': 'purple'}
```

## 🔧 Troubleshooting

### Common Issues:

1. **WiFi Connection Fails**
   - Check WiFi credentials
   - Ensure WiFi network is 2.4GHz (ESP32 doesn't support 5GHz)
   - Check signal strength

2. **Server Connection Fails**
   - Verify Mac server is running
   - Check IP address is correct
   - Ensure both devices are on same network
   - Check firewall settings

3. **Library Import Errors**
   - Verify all required libraries are in `/lib/` folder
   - Check library compatibility with CircuitPython version

4. **ESP32 Communication Issues**
   - Check physical connections
   - Verify ESP32 firmware is up to date
   - Try power cycling the board

## 📚 Next Steps

Once the basic WiFi proof of concept works:

1. **Add Sensors**: Send sensor data to the server
2. **Real-time Updates**: Create continuous data streaming
3. **Web Interface**: Build a web dashboard
4. **Database**: Store data in a database
5. **Cloud Integration**: Send data to cloud services

## 🎯 Success Criteria

✅ Metro M4 connects to WiFi  
✅ Metro M4 can reach Mac server  
✅ Metro M4 can send data to server  
✅ Mac server receives and displays data  
✅ NeoPixel shows correct status colors  
✅ All steps complete without errors
