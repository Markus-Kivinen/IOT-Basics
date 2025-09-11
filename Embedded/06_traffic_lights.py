from machine import Pin
import utime

led_red = Pin(15, Pin.OUT)
led_yellow = Pin(14, Pin.OUT)
led_green = Pin(13, Pin.OUT)
leds = [
    # Pin / Seconds
    [led_red, 2],
    [led_yellow, 2],
    [led_green, 5],
    [led_yellow, 2],
]
button = Pin(16, Pin.IN, Pin.PULL_DOWN)
buzzer = Pin(12, Pin.OUT)

state = 0

while True:
    if button.value() == 1:
        led_red.value(0)
        led_red.value(0)
        led_green.value(1)
        for i in range(10):
            buzzer.value(1)
            utime.sleep(0.2)
            buzzer.value(0)
            utime.sleep(0.2)
        led_green.value(0)
        state = 0
    pin, duration = leds[state]
    pin.value(1)
    utime.sleep(duration)
    pin.value(0)
    state = (state + 1) % len(leds)