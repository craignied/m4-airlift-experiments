# Metro M4 Airlift Lite - Hello World Guide

## Overview
The Metro M4 Airlift Lite is a powerful microcontroller board from Adafruit featuring:
- **Microcontroller**: SAMD51 (ARM Cortex-M4)
- **WiFi**: ESP32 co-processor for WiFi connectivity
- **CircuitPython**: Python-based programming environment
- **Built-in LED**: Connected to pin D13
- **USB-C**: For programming and power

## Prerequisites
1. **Metro M4 Airlift Lite board**
2. **USB-C cable**
3. **Computer** (Windows, Mac, or Linux)
4. **CircuitPython firmware** (download from Adafruit)
5. **Cursor IDE** with CircuitPython v2 extension (✅ Already installed!)

## Step 1: Install CircuitPython

1. **Download CircuitPython**:
   - Visit [circuitpython.org](https://circuitpython.org/)
   - Find "Metro M4 Airlift Lite" in the board list
   - Download the latest `.uf2` file

2. **Enter Bootloader Mode**:
   - Double-click the reset button on your Metro M4
   - The board should appear as a USB drive named `METROM4AIRLIFTBOOT`

3. **Install CircuitPython**:
   - Copy the downloaded `.uf2` file to the `METROM4AIRLIFTBOOT` drive
   - The board will automatically restart and appear as `CIRCUITPY`

## Step 2: Development with Cursor IDE

Since you have CircuitPython v2 installed in Cursor, you can develop directly in the IDE:

### Setting up Cursor for CircuitPython Development
1. **Open CircuitPython Extension**: Look for the CircuitPython extension in Cursor
2. **Connect Your Board**: Plug in your Metro M4 Airlift Lite
3. **Select Device**: Choose your board from the device list in the extension
4. **Create Project**: Start a new project or open an existing one

### Cursor-Specific Features
- **Integrated Serial Monitor**: View output directly in Cursor
- **REPL Access**: Interactive Python shell for testing
- **Auto-save to Board**: Save files directly to the CIRCUITPY drive
- **Library Management**: Easy installation of CircuitPython libraries
- **Syntax Highlighting**: Full Python syntax support

## Step 3: Create Hello World Program

### Basic Hello World (Serial Output)
Create a file named `code.py` on the `CIRCUITPY` drive:

```python
# Hello World for Metro M4 Airlift Lite
import time

print("Hello, World!")
print("Welcome to Metro M4 Airlift Lite!")

# Blink the built-in LED
import board
import digitalio

# Set up the built-in LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

print("Starting LED blink demo...")

while True:
    led.value = True  # Turn on LED
    print("LED ON")
    time.sleep(1)
    
    led.value = False  # Turn off LED
    print("LED OFF")
    time.sleep(1)
```

### Hello World with WiFi (Advanced)
For a more advanced hello world that demonstrates WiFi capabilities:

```python
# Hello World with WiFi for Metro M4 Airlift Lite
import time
import board
import digitalio
import wifi
import socketpool
import ssl
import adafruit_requests

# Set up the built-in LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

print("Metro M4 Airlift Lite Hello World!")
print("Connecting to WiFi...")

# Configure WiFi (replace with your network details)
WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"

try:
    wifi.radio.start_ap(WIFI_SSID, WIFI_PASSWORD)
    print(f"Connected to {WIFI_SSID}")
    
    # Blink LED to show WiFi connection
    for i in range(3):
        led.value = True
        time.sleep(0.2)
        led.value = False
        time.sleep(0.2)
    
    # Get IP address
    ip_address = wifi.radio.ipv4_address
    print(f"IP Address: {ip_address}")
    
except Exception as e:
    print(f"WiFi connection failed: {e}")

# Main loop
while True:
    led.value = True
    print("Hello from Metro M4 Airlift Lite!")
    time.sleep(2)
    
    led.value = False
    print("LED blinking...")
    time.sleep(2)
```

## Step 3: Viewing Output

### Method 1: Serial Monitor
1. Open a serial monitor (like PuTTY, Screen, or Arduino IDE)
2. Connect to the COM port (Windows) or `/dev/ttyACM0` (Linux/Mac)
3. Set baud rate to 115200
4. You should see the hello world messages

### Method 2: Mu Editor
1. Download Mu Editor from [codewith.mu](https://codewith.mu/)
2. Open Mu and select "CircuitPython"
3. Connect your board
4. Click the "Serial" button to see output

### Method 3: Thonny IDE
1. Install Thonny IDE
2. Configure for CircuitPython
3. Connect to your board
4. Use the Shell to see print statements

## Step 4: Troubleshooting

### Common Issues:
1. **Board not recognized**: Try a different USB cable
2. **No CIRCUITPY drive**: Reinstall CircuitPython firmware
3. **Code not running**: Ensure file is named `code.py`
4. **No serial output**: Check baud rate and COM port

### Reset Options:
- **Soft reset**: Press Ctrl+C in serial monitor
- **Hard reset**: Double-click reset button
- **Factory reset**: Hold reset button for 10 seconds

## Next Steps

After getting hello world working, you can explore:
1. **WiFi connectivity** with HTTP requests
2. **Sensors** (if connected)
3. **Display** projects
4. **IoT** applications
5. **Web server** functionality

## File Structure
```
CIRCUITPY/
├── code.py          # Main program (auto-runs)
├── lib/             # Libraries folder
├── boot.py          # Boot configuration
└── settings.toml    # WiFi settings
```

## Resources
- [CircuitPython Documentation](https://docs.circuitpython.org/)
- [Adafruit Metro M4 Airlift Lite Guide](https://learn.adafruit.com/adafruit-metro-m4-express-airlift-lite)
- [CircuitPython Libraries](https://circuitpython.org/libraries)

Happy coding with your Metro M4 Airlift Lite! 🚀

## 🚀 Bonus: Cursor IDE Development Tips

Since you have CircuitPython v2 installed in Cursor, here are some pro tips:

### Quick Start with Cursor
1. **Open CircuitPython Extension**: Look for the CircuitPython extension in Cursor
2. **Connect Your Board**: Plug in your Metro M4 Airlift Lite
3. **Select Device**: Choose your board from the device list
4. **Create `code.py`**: Start coding directly in Cursor

### Cursor-Specific Features
- **Integrated Serial Monitor**: View output directly in Cursor
- **REPL Access**: Interactive Python shell for testing
- **Auto-save to Board**: Save files directly to the CIRCUITPY drive
- **Library Management**: Easy installation of CircuitPython libraries
- **Syntax Highlighting**: Full Python syntax support
- **IntelliSense**: Code completion and error detection

### Recommended Workflow
1. Write your code in Cursor
2. Save the file (it auto-saves to your board)
3. Use the integrated serial monitor to see output
4. Use REPL for quick testing and debugging
5. Iterate and improve!

This makes development much faster and more efficient than traditional methods!

## 🎯 Key Learnings from This Session

### LED Confusion Resolution
- **Green LED blinking every 5 seconds** = CircuitPython status indicator (normal behavior)
- **Tiny "L" LED** = User-controllable LED (works with `board.LED`)
- **Large RGB NeoPixel LED** = The main programmable LED (what we wanted to control)

### NeoPixel Library Issues
- **Old neopixel.mpy from 2019** = Incompatible with CircuitPython 9.2.8
- **Solution**: Download CircuitPython 9.x bundle and use the correct `neopixel.mpy`
- **Library location**: `/Volumes/CIRCUITPY/lib/neopixel.mpy`

### Working NeoPixel Program
- **File**: `neopixel_purple_blink.py` (saved in main directory)
- **Features**: Purple blinking NeoPixel LED every second
- **Uses**: `board.NEOPIXEL` pin and `neopixel.NeoPixel()` class

### CircuitPython Error Indicators
- **Green LED blinking every 5 seconds** = Normal operation
- **Two red flashes every 5 seconds** = Code ended due to exception
- **Different blink patterns** = Various error conditions

### Development Tips
- **Hardware reset** (unplug/plug) often fixes library issues
- **Check library compatibility** with CircuitPython version
- **Use CircuitPython bundles** for compatible libraries
- **Look at the right LED** - NeoPixel vs status LED vs tiny "L" LED
