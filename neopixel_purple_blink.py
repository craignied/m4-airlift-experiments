# Hello World for Metro M4 Airlift Lite
# NeoPixel Purple Blink Program

import time
import board
import neopixel

print("Hello World!")
print("Metro M4 Airlift Lite - NeoPixel Purple Blink")

# Set up the NeoPixel LED
# The Metro M4 Airlift Lite has 1 NeoPixel LED
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

print("NeoPixel setup complete")

# Define purple color (Red, Green, Blue)
PURPLE = (128, 0, 128)  # Nice purple color
OFF = (0, 0, 0)         # Turn off

print("Starting purple NeoPixel blink...")

# Blink the NeoPixel in purple
while True:
    pixel[0] = PURPLE  # Turn on purple
    print("NeoPixel ON - Purple")
    time.sleep(1)
    
    pixel[0] = OFF     # Turn off
    print("NeoPixel OFF")
    time.sleep(1)
