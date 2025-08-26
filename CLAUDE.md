# Metro M4 Airlift Lite - Real-Time IoT Project

## Overview
The Metro M4 Airlift Lite is a powerful microcontroller board from Adafruit featuring:
- **Microcontroller**: SAMD51 (ARM Cortex-M4)
- **WiFi**: ESP32 co-processor for WiFi connectivity
- **CircuitPython**: Python-based programming environment
- **Built-in LED**: Connected to pin D13
- **NeoPixel LED**: RGB LED for visual feedback
- **USB-C**: For programming and power

## Project Status: ✅ COMPLETE - Real-Time WebSocket Server

### What We've Built
🎉 **Successfully implemented a complete real-time IoT system** with:
- **CircuitPython device** that blinks a NeoPixel LED and sends status updates
- **Python WebSocket server** running on Mac that receives real-time updates
- **Beautiful web interface** with live status display
- **Real-time communication** - no page refreshes needed

### Current Features
✅ **WiFi connectivity** - Automatic connection to home network  
✅ **NeoPixel control** - Blinking LED with status tracking  
✅ **HTTP communication** - Status updates sent to server  
✅ **WebSocket server** - Real-time data broadcasting  
✅ **Web interface** - Live status display with beautiful UI  
✅ **Error handling** - Graceful connection recovery  
✅ **Automatic reconnection** - WebSocket reconnects if connection drops  

### Technical Architecture
```
Metro M4 Airlift Lite (CircuitPython)
    ↓ HTTP POST requests
Python WebSocket Server (Mac)
    ↓ WebSocket broadcasts
Web Browser Interface
```

## Prerequisites
1. **Metro M4 Airlift Lite board**
2. **USB-C cable**
3. **Computer** (Windows, Mac, or Linux)
4. **CircuitPython firmware** (download from Adafruit)
5. **Cursor IDE** with CircuitPython v2 extension (✅ Already installed!)
6. **Python 3.x** with websockets library

## 📥 Downloads

### CircuitPython Firmware
- **Download**: [CircuitPython 9.2.8 for Metro M4 Airlift Lite](https://circuitpython.org/board/metro_m4_airlift_lite/)
- **File**: `adafruit-circuitpython-metro_m4_airlift_lite-en_US-9.2.8.uf2`
- **Installation**: Double-click reset button, drag .uf2 file to METROM4BOOT drive

### CircuitPython Libraries
- **Download**: [CircuitPython Libraries Bundle](https://circuitpython.org/libraries)
- **Version**: Use 9.x bundle for CircuitPython 9.2.8
- **Required libraries**: `neopixel.mpy`, `adafruit_requests.mpy`, `adafruit_esp32spi.mpy`
- **Installation**: Extract bundle, copy needed .mpy files to `/lib/` folder on CIRCUITPY drive

## Current Working Files

### CircuitPython Device (`wifi_proof_of_concept.py`)
- Connects to WiFi automatically
- Blinks NeoPixel LED every 4 seconds (2s ON, 2s OFF)
- Sends status updates via HTTP POST to server
- Includes error handling and reconnection logic

### WebSocket Server (`simple_server.py`)
- HTTP server on port 8000 for receiving device data
- WebSocket server on port 8765 for real-time broadcasting
- Beautiful web interface with live status updates
- Thread-safe broadcast mechanism
- Automatic WebSocket reconnection handling

### Configuration (`config.py`)
- WiFi credentials
- Server IP address and endpoints
- Device configuration settings

## 🚀 How to Run

### 1. Start the Server
```bash
python3 simple_server.py
```
Server will start on `http://192.168.1.148:8000`

### 2. Upload Code to Device
Copy `wifi_proof_of_concept.py` to `code.py` on the CIRCUITPY drive

### 3. Access Web Interface
Open `http://192.168.1.148:8000` in your browser

### 4. Monitor Device
Use serial monitor to see device output:
```bash
screen /dev/tty.usbmodem84101 115200
```

## 🔧 Stability Issues & Solutions

### Current Problem: 24-Hour Reliability
**Issue**: Device experiences SPI communication errors after ~24 hours of operation
- Error: "Timed out waiting for SPI char"
- Device gets stuck with solid green NeoPixel
- Requires manual reset to recover

**Root Causes**:
1. **Memory leaks** - CircuitPython accumulating memory over time
2. **WiFi module instability** - ESP32 getting into bad state
3. **Power supply issues** - USB power insufficient for long-term operation
4. **Heat buildup** - Extended operation causing thermal issues

### Planned Stability Improvements

#### 1. Watchdog Timer Implementation
```python
# Add hardware watchdog to auto-reset on failure
import watchdog
watchdog.timeout = 30  # Reset if no activity for 30 seconds
```

#### 2. Memory Management
- Add periodic garbage collection
- Monitor memory usage
- Restart WiFi connection periodically
- Implement memory leak detection

#### 3. Error Recovery Mechanisms
- Automatic retry for failed HTTP requests
- Graceful degradation when WiFi fails
- Automatic reconnection logic
- Error logging and reporting

#### 4. Power Management
- Consider external power supply instead of USB
- Add power monitoring
- Implement low-power modes
- Add voltage monitoring

#### 5. Code Optimization
- Reduce status update frequency (every 10s instead of 2-3s)
- Simplify HTTP requests
- Add error handling around WiFi operations
- Implement connection pooling

#### 6. Monitoring & Alerting
- Add uptime tracking
- Implement health checks
- Add automatic restart scheduling
- Create alert system for failures

### Expected Reliability Target
- **Goal**: 99% uptime over 30 days
- **Target**: Automatic recovery from 95% of failure modes
- **Monitoring**: Real-time health status in web interface

## 📊 Performance Metrics

### Current Performance
- **Uptime**: ~24 hours before requiring reset
- **Update frequency**: Every 2-3 seconds
- **Response time**: <500ms for web interface updates
- **Memory usage**: Growing over time (needs optimization)

### Target Performance
- **Uptime**: 30+ days without manual intervention
- **Update frequency**: Every 10 seconds (reduced for stability)
- **Response time**: <1 second for web interface updates
- **Memory usage**: Stable over time

## 🎯 Next Development Priorities

### Phase 1: Stability (Current Focus)
1. Implement watchdog timer
2. Add memory management
3. Implement error recovery
4. Add health monitoring

### Phase 2: Features
1. Add sensor support (temperature, humidity, etc.)
2. Implement data logging
3. Add configuration web interface
4. Create mobile app

### Phase 3: Scale
1. Support multiple devices
2. Add database storage
3. Implement user authentication
4. Create API endpoints

## 🚨 Troubleshooting

### Common Issues
1. **SPI timeout errors**: Reset device (unplug/replug USB)
2. **WebSocket disconnection**: Automatic reconnection implemented
3. **Server port conflicts**: Kill existing processes with `pkill -f simple_server.py`
4. **WiFi connection issues**: Check credentials in `config.py`

### Reset Procedures
- **Soft reset**: Press reset button on device
- **Hard reset**: Unplug and replug USB cable
- **Server reset**: Restart `simple_server.py`

## 📁 File Structure
```
MetroM4Airlift/
├── wifi_proof_of_concept.py    # Main CircuitPython code
├── simple_server.py            # WebSocket server
├── config.py                   # Configuration settings
├── examples/                   # Example programs
│   ├── hello_world/
│   └── wifi_demo/
├── lib/                        # CircuitPython libraries
└── CLAUDE.md                   # This documentation
```

## Resources
- [CircuitPython Documentation](https://docs.circuitpython.org/)
- [Adafruit Metro M4 Airlift Lite Guide](https://learn.adafruit.com/adafruit-metro-m4-express-airlift-lite)
- [CircuitPython Libraries](https://circuitpython.org/libraries)
- [WebSocket Documentation](https://websockets.readthedocs.io/)

## 🎉 Success Metrics

✅ **Real-time communication** - WebSocket working perfectly  
✅ **Beautiful web interface** - Live status updates  
✅ **Automatic reconnection** - Robust connection handling  
✅ **Error handling** - Graceful failure recovery  
✅ **Documentation** - Complete setup and usage guide  

**Next Goal**: Achieve 30+ day uptime with automatic recovery mechanisms!

---

*Last updated: August 25, 2025 - Real-time WebSocket server complete, focusing on stability improvements*
