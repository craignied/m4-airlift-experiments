# Community-Proven WiFi Solution for Metro M4 Airlift Lite
# Based on web search findings - uses esp.reset() and proper error handling

import time
import board
import busio
import digitalio
import neopixel
from adafruit_esp32spi import adafruit_esp32spi

# Import WiFi credentials
try:
    from config import WIFI_SSID, WIFI_PASSWORD, SERVER_IP, SERVER_PORT
    print("✅ Config loaded successfully")
except ImportError as e:
    print(f"❌ Error loading config: {e}")
    WIFI_SSID = "csn8744"
    WIFI_PASSWORD = "1428cf4891"
    SERVER_IP = "192.168.1.192"  # Correct server IP
    SERVER_PORT = "8000"
    print("⚠️ Using fallback credentials")

print("🚀 Community-Proven WiFi Solution Starting...")

# Set up NeoPixel for status indication
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.3

# Colors for status
OFF = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

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
    esp.connect_AP(WIFI_SSID, WIFI_PASSWORD)
    print("✅ WiFi connected!")
    show_status(GREEN, "WiFi connected!")
    
    # Get IP address
    print(f"🌐 My IP address: {esp.pretty_ip(esp.ip_address)}")
    
    # Setup requests
    import adafruit_esp32spi.adafruit_esp32spi_socketpool as socketpool
    import adafruit_requests
    
    pool = socketpool.SocketPool(esp)
    requests_session = adafruit_requests.Session(pool)
    
    server_url = f"http://{SERVER_IP}:{SERVER_PORT}"
    print(f"🔗 Server URL: {server_url}")
    
    print("🚀 Starting continuous NeoPixel blinking with community-proven error recovery...")
    
    blink_count = 0
    
    while True:
        try:
            # Memory cleanup every 10 cycles
            if blink_count % 10 == 0:
                try:
                    import gc
                    gc.collect()
                    print(f"🧹 Memory cleanup - Count: {blink_count}")
                except:
                    pass
            
            # Turn NeoPixel ON
            show_status(GREEN, "ON")
            print(f"💡 NeoPixel ON - Count: {blink_count}")
            
            # Send ON status to server
            status_data = {
                "status": "ON",
                "count": blink_count,
                "board": "Metro M4 Airlift Lite",
                "ip_address": esp.pretty_ip(esp.ip_address),
                "timestamp": time.time()
            }
            
            try:
                response = requests_session.post(f"{server_url}/status", json=status_data)
                response.close()
                print("✅ ON status sent successfully")
            except (ValueError, RuntimeError, ConnectionError, OSError) as e:
                print(f"⚠️ ESP has an issue, resetting and retrying: {e}")
                show_status(PURPLE, "Resetting ESP32...")
                
                # Community-proven reset sequence
                esp.reset()
                esp.disconnect()
                time.sleep(5)  # Wait for ESP32 to boot
                esp.connect_AP(WIFI_SSID, WIFI_PASSWORD)
                show_status(GREEN, "ESP32 reset complete!")
                
                # Retry the request after successful reset
                try:
                    response = requests_session.post(f"{server_url}/status", json=status_data)
                    response.close()
                    print("✅ ON status sent after reset")
                except Exception as retry_e:
                    print(f"❌ Still failed after reset: {retry_e}")
            
            time.sleep(2)  # Stay ON for 2 seconds
            
            # Turn NeoPixel OFF
            show_status(OFF, "OFF")
            print(f"💡 NeoPixel OFF - Count: {blink_count}")
            
            # Send OFF status to server
            status_data["status"] = "OFF"
            try:
                response = requests_session.post(f"{server_url}/status", json=status_data)
                response.close()
                print("✅ OFF status sent successfully")
            except (ValueError, RuntimeError, ConnectionError, OSError) as e:
                print(f"⚠️ ESP has an issue, resetting and retrying: {e}")
                show_status(PURPLE, "Resetting ESP32...")
                
                # Community-proven reset sequence
                esp.reset()
                esp.disconnect()
                time.sleep(5)  # Wait for ESP32 to boot
                esp.connect_AP(WIFI_SSID, WIFI_PASSWORD)
                show_status(GREEN, "ESP32 reset complete!")
                
                # Retry the request after successful reset
                try:
                    response = requests_session.post(f"{server_url}/status", json=status_data)
                    response.close()
                    print("✅ OFF status sent after reset")
                except Exception as retry_e:
                    print(f"❌ Still failed after reset: {retry_e}")
            
            time.sleep(2)  # Stay OFF for 2 seconds
            
            blink_count += 1
            
        except Exception as e:
            print(f"❌ Error in blink loop: {e}")
            show_status(RED, f"Error: {type(e).__name__}")
            
            # Try to reset and reconnect on any major error
            try:
                print("🔄 Attempting ESP32 reset and recovery...")
                show_status(PURPLE, "Resetting ESP32...")
                esp.reset()
                esp.disconnect()
                time.sleep(5)
                esp.connect_AP(WIFI_SSID, WIFI_PASSWORD)
                show_status(GREEN, "Recovery successful!")
                print("✅ Recovery successful, continuing...")
            except Exception as recovery_e:
                print(f"❌ Recovery failed: {recovery_e}")
                time.sleep(10)
    
except Exception as e:
    print(f"❌ Error: {e}")
    show_status(RED, f"Error: {e}")
    
    # Keep the red light on for 5 seconds
    time.sleep(5)

print("🏁 WiFi test complete!")
show_status(OFF, "Test complete")


