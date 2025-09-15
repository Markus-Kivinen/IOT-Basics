from machine import Pin
import network
import utime
import urequests
import dht

API_KEY = "************"

print("Connecting to WiFi", end="")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Wokwi-GUEST", "")
while not wlan.isconnected():
  print(".", end="")
  utime.sleep(0.1)
print(" Connected!")

sensor = dht.DHT22(Pin(15))
while True:
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        API_URL = f'https://api.thingspeak.com/update?api_key={API_KEY}&field1={temperature}&field2={humidity}'
        print(f"Temperature: {temperature:.1f}°C\nHumidity: {humidity:.1f}%")
        r = urequests.get(API_URL)
    except OSError as e:
        print("Sensor read error:", e)
    utime.sleep(2)
