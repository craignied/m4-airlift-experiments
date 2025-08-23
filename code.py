# Hello World for Metro M4 Airlift Lite
# LED Blink Program (tiny L LED)

import time
import board
import digitalio

print("Hello World!")
print("Metro M4 Airlift Lite - LED Blink")

# Set up the built-in LED (the tiny "L" LED)
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

print("LED setup complete")
print("Watch the tiny 'L' LED on the board")

# Blink the LED
while True:
    led.value = True
    print("LED ON")
    time.sleep(1)
    
    led.value = False
    print("LED OFF")
    time.sleep(1)
