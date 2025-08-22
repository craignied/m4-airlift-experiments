# Hello World for Metro M4 Airlift Lite
# Basic example with LED blinking and serial output

import time
import board
import digitalio

print("Hello, World!")
print("Welcome to Metro M4 Airlift Lite!")
print("Starting LED blink demo...")

# Set up the built-in LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Main loop
while True:
    led.value = True  # Turn on LED
    print("LED ON")
    time.sleep(1)
    
    led.value = False  # Turn off LED
    print("LED OFF")
    time.sleep(1)
