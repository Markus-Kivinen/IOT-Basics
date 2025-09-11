import time
from machine import Pin

time.sleep(0.1)

led = Pin(18, Pin.OUT)
button = Pin(13, Pin.IN, Pin.PULL_UP)
while True:
    if button.value():
        led.value(0)
    else:
        led.value(1)
