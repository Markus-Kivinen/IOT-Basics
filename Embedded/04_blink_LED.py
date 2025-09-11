import time
from machine import Pin

time.sleep(0.1)

led = Pin(15, Pin.OUT)

while True:
    led.toggle()
    time.sleep(1)
