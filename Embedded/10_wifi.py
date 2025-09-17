from machine import Pin
import network
import utime
import urequests
import dht

API_KEY = "************"
API_BASE_URL = "https://api.thingspeak.com/update"
ssid = "Wokwi-GUEST"
password = ""

print("Connecting to WiFi", end="")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while not wlan.isconnected():
    print(".", end="")
    utime.sleep(0.1)
print(" Connected!")

sensor = dht.DHT22(Pin(15))
while True:
    try:
        sensor.measure()
        temp: float = sensor.temperature()
        humidity: float = sensor.humidity()
        print(f"Temperature: {temp:.1f}°C\nHumidity: {humidity:.1f}%")
        API_URL = (
            f'{API_BASE_URL}?api_key={API_KEY}'
            f'&field1={temp}&field2={humidity}'
        )
        urequests.get(API_URL)
    except OSError as e:
        print("Sensor read error:", e)
    utime.sleep(2)
