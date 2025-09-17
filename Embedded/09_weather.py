import dht
import utime
from machine import Pin

sensor = dht.DHT22(Pin(15))

while True:
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        print(f"Temperature: {temperature:.1f}°C, Humidity: {humidity:.1f}%")
    except OSError as e:
        print("Sensor read error:", e)
    utime.sleep(2)
