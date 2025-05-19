from machine import Pin, I2C
import network
import time
import urequests
from ssd1306 import SSD1306_I2C

# Configurar I2C y pantalla OLED
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(128, 32, i2c)

# Conexión WiFi
def conectaWifi(red, password):
    miRed = network.WLAN(network.STA_IF)
    if not miRed.isconnected():
        miRed.active(True)
        miRed.connect(red, password)
        print("Conectando a la red", red)
        timeout = time.time()
        while not miRed.isconnected():
            if (time.ticks_diff(time.time(), timeout) > 10):
                print("No se pudo conectar.")
                return False
            time.sleep(1)
    print("¡Conectado!", miRed.ifconfig())
    return True

# Leer último dato de ThingSpeak
def obtenerDatos():
    try:
        url = "https://api.thingspeak.com/channels/2937444/feeds.json?api_key=M4YOW4Y14XQ6N2IE&results=1"
        respuesta = urequests.get(url)
        datos = respuesta.json()

        feeds = datos["feeds"]
        if feeds:
            ultimo = feeds[-1]
            temp = ultimo["field1"]
            hum = ultimo["field2"]
            pres = ultimo["field3"]
            ca = ultimo["field4"]
            luz = ultimo["field5"]
            respuesta.close()
            return temp, hum, pres, ca, luz
        else:
            return None, None, None, None, None
    except Exception as e:
        print("Error:", e)
        return None, None, None, None, None

# Conectar WiFi y mostrar datos rotando
if conectaWifi("Wokwi-GUEST", ""):
    while True:
        temp, hum, pres, ca, luz = obtenerDatos()
        if temp and hum and pres and ca and luz:
            # Pantalla 1: Temperatura y Humedad
            oled.fill(0)
            oled.text("Temperatura: {}C".format(temp), 0, 0)
            oled.text("Humedad: {}%".format(hum), 0, 10)
            oled.show()
            time.sleep(5)

            # Pantalla 2: Presión y Calidad del Aire
            oled.fill(0)
            oled.text("Presion: {} hPa".format(pres), 0, 0)
            oled.text("Cal.Aire: {} ppm".format(ca), 0, 10)
            oled.show()
            time.sleep(5)

            # Pantalla 3: Luz
            oled.fill(0)
            oled.text("Luz: {} lux".format(luz), 0, 0)
            oled.show()
            time.sleep(5)
        else:
            oled.fill(0)
            oled.text("Error al leer", 0, 0)
            oled.text("los datos", 0, 10)
            oled.show()
            time.sleep(5)
