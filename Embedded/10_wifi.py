import dht
import network
import urequests
import utime
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C  # pyright: ignore[reportMissingImports]

API_URL = "http://192.168.50.147:8000/api/sensor"
ssid = "Wokwi-GUEST"
password = ""

sensor = dht.DHT22(Pin(22))
i2c_dev = I2C(1, scl=Pin(27), sda=Pin(26), freq=200000)
oled = SSD1306_I2C(128, 64, i2c_dev)

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
        oled.text(f"Temp: {temp:.1f}C", 5, 5)
        oled.text(f"Humidity: {humidity:.1f}%", 5, 15)
        oled.show()
        r = urequests.post(
           API_URL,
           json={"temperature": temp, "humidity": humidity, "status": "OK"},
           headers={"Content-Type": "application/json"},
        )
        r.close()
    except OSError as e:
        print("Sensor read error:", e)
    utime.sleep(10)
