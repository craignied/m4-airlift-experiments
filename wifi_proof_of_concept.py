# Simple WiFi Test for Metro M4 Airlift Lite
# Just tests basic WiFi connection

import time
import board
import busio
import digitalio
import neopixel
from adafruit_esp32spi import adafruit_esp32spi

# Import WiFi credentials from separate file
try:
    from config import WIFI_SSID, WIFI_PASSWORD
    print("✅ Config loaded successfully")
except ImportError as e:
    print(f"❌ Error loading config: {e}")
    # Fallback to hardcoded credentials (replace with your actual values)
    WIFI_SSID = "csn8744"
    WIFI_PASSWORD = "1428cf4891"
    print("⚠️ Using fallback credentials")

print("🚀 Simple WiFi Test Starting...")

# Set up NeoPixel for status indication
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.3

# Colors for status
OFF = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def show_status(color, message):
    """Show status on NeoPixel and print message"""
    pixel[0] = color
    print(f"💡 {message}")

# ESP32 Setup
esp32_cs = digitalio.DigitalInOut(board.ESP_CS)
esp32_ready = digitalio.DigitalInOut(board.ESP_BUSY)
esp32_reset = digitalio.DigitalInOut(board.ESP_RESET)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

print("📡 ESP32 setup complete")

# Test WiFi connection
print(f"🔗 Connecting to WiFi: {WIFI_SSID}")
show_status(YELLOW, "Connecting to WiFi...")

try:
    print(f"🔍 Attempting to connect to SSID: {WIFI_SSID}")
    print(f"🔍 Password length: {len(WIFI_PASSWORD)}")
    
    # Try to connect
    esp.connect_AP(WIFI_SSID, WIFI_PASSWORD)
    print("✅ WiFi connected!")
    show_status(GREEN, "WiFi connected!")
    
    # Get IP address
    print(f"🌐 My IP address: {esp.pretty_ip(esp.ip_address)}")
    
    # Test server connection
    print("🔧 Setting up HTTP requests...")
    import adafruit_requests
    
    # Get server info from config
    try:
        from config import SERVER_IP, SERVER_PORT
        server_url = f"http://{SERVER_IP}:{SERVER_PORT}"
        print(f"🔗 Testing connection to: {server_url}")
        
        # Create requests session using socketpool
        import adafruit_esp32spi.adafruit_esp32spi_socketpool as socketpool
        pool = socketpool.SocketPool(esp)
        requests = adafruit_requests.Session(pool)
        
        # Test simple GET request first
        print("📤 Sending simple GET request...")
        response = requests.get(f"{server_url}/")
        
        if response.status_code == 200:
            print("✅ Server connection successful!")
            try:
                print("📥 Reading response...")
                print("📄 Response status code:", response.status_code)
                print("📄 Response headers:", response.headers)
                
                # For now, skip reading content to avoid hanging
                print("✅ HTTP GET request successful!")
                print("💡 Skipping content reading to avoid timeout")
                
                # Now try a POST request to send data
                print("📤 Sending POST request with data...")
                hello_data = {
                    "message": "Hello from Metro M4 Airlift Lite!",
                    "board": "Metro M4 Airlift Lite",
                    "ip_address": esp.pretty_ip(esp.ip_address),
                    "status": "WiFi connected and HTTP working"
                }
                
                post_response = requests.post(f"{server_url}/data", json=hello_data)
                print(f"📄 POST Response status: {post_response.status_code}")
                
                if post_response.status_code == 200:
                    print("✅ Hello world sent successfully!")
                else:
                    print(f"❌ POST request failed: {post_response.status_code}")
                    
                post_response.close()
                
            except Exception as e:
                print(f"❌ Error reading response: {e}")
            finally:
                print("🔒 Closing response...")
                response.close()
        else:
            print(f"❌ Server connection failed: {response.status_code}")
            response.close()
            
    except Exception as e:
        print(f"❌ Server test error: {e}")
    
    # Keep the green light on for 5 seconds
    time.sleep(5)
    
except Exception as e:
    print(f"❌ Error: {e}")
    show_status(RED, f"Error: {e}")
    
    # Keep the red light on for 5 seconds
    time.sleep(5)

print("🏁 WiFi test complete!")
show_status(OFF, "Test complete")
