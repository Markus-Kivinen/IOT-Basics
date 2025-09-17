import time

from machine import Pin

motion = Pin(28, Pin.OUT)

while True:
    if motion.value():
        print("Motion detected")
    time.sleep(1)
