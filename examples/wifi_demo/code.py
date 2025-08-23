# WiFi Demo for Metro M4 Airlift Lite
# Advanced example showing WiFi connectivity and HTTP requests

import time
import board
import digitalio
import wifi
import socketpool
import ssl
import adafruit_requests

print("Metro M4 Airlift Lite WiFi Demo!")
print("Connecting to WiFi...")

# Set up the built-in LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Configure WiFi (replace with your network details)
WIFI_SSID = "csn8744"
WIFI_PASSWORD = "1428cf4891"

try:
    # Connect to WiFi
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
    
    # Set up HTTP requests
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    
    # Make a test HTTP request
    print("Making HTTP request to httpbin.org...")
    response = requests.get("https://httpbin.org/get")
    print(f"Response status: {response.status_code}")
    print(f"Response: {response.text[:100]}...")  # First 100 characters
    
except Exception as e:
    print(f"WiFi connection failed: {e}")

# Main loop
counter = 0
while True:
    led.value = True
    print(f"Hello from Metro M4 Airlift Lite! Counter: {counter}")
    time.sleep(2)
    
    led.value = False
    print("LED blinking...")
    time.sleep(2)
    
    counter += 1
