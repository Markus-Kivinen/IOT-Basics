import time
from machine import Pin

time.sleep(0.1)

led = Pin("LED", Pin.OUT)
while True:
    led.toggle()
    time.sleep(1)
