# WiFi Demo Example

An advanced CircuitPython example for the Metro M4 Airlift Lite that demonstrates:
- WiFi connectivity
- HTTP requests
- LED status indicators
- Error handling

## What it does

This example:
1. Connects to a WiFi network
2. Makes an HTTP request to httpbin.org
3. Blinks the LED to show status
4. Continues running with a counter

## Prerequisites

You need the following CircuitPython libraries in your `lib` folder:
- `adafruit_requests.mpy`
- `adafruit_esp32spi.mpy` (if using ESP32)

## Configuration

Before running, update the WiFi credentials in `code.py`:

```python
WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"
```

## How to use

1. Install required libraries in your `lib` folder
2. Update WiFi credentials in `code.py`
3. Copy `code.py` to your `CIRCUITPY` drive
4. Open a serial monitor (115200 baud)
5. Watch the connection process and HTTP request

## Expected output

```
Metro M4 Airlift Lite WiFi Demo!
Connecting to WiFi...
Connected to your_wifi_ssid
IP Address: 192.168.1.100
Making HTTP request to httpbin.org...
Response status: 200
Response: {"args":{},"headers":{"Accept":"*/*","Accept-Encoding":"gzip, deflate"...
Hello from Metro M4 Airlift Lite! Counter: 0
LED blinking...
...
```

## Hardware

- Metro M4 Airlift Lite board
- Built-in LED (no additional hardware needed)
- WiFi network access

## Troubleshooting

- Make sure your WiFi credentials are correct
- Check that you have the required libraries installed
- Ensure your WiFi network is accessible
