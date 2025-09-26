import dht
import network
import urequests
import utime
from machine import Pin

API_URL = "http://maketti-spagetti.loca.lt/api/sensor"
ssid = "Wokwi-GUEST"
password = ""

sensor = dht.DHT22(Pin(15))

print("Connecting to WiFi", end="")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while not wlan.isconnected():
    print(".", end="")
    utime.sleep(0.1)
print(" Connected!")

while True:
    try:
        sensor.measure()
        temp: float = sensor.temperature()
        humidity: float = sensor.humidity()
        print(f"Temperature: {temp:.1f}C, Humidity: {humidity:.1f}%")
        r = urequests.post(
            API_URL,
            json={"temperature": temp, "humidity": humidity, "status": "OK"},
            headers={"Content-Type": "application/json"},
        )
        r.close()
    except OSError as e:
        print("Sensor read error:", e)
    utime.sleep(10)
