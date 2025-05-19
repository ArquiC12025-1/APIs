from machine import Pin
import time, urequests, network
import random

# Función para conectar el ESP32 a una red WiFi
def conectaWifi(red, password):
    miRed = network.WLAN(network.STA_IF)
    if not miRed.isconnected():
        miRed.active(True)
        miRed.connect(red, password)
        print("Conectando a la red", red + "...")
        timeout = time.time()
        while not miRed.isconnected():
            if (time.ticks_diff(time.time(), timeout) > 10):
                print("Error: No se pudo conectar a la red.")
                return False
            time.sleep(1)
    return True

# Función para enviar datos a ThingSpeak
def enviarDatos(temp, hum, presion, calidad_aire, luz):
    url = "https://api.thingspeak.com/update?api_key=M4YOW4Y14XQ6N2IE"
    query_string = f"&field1={temp}&field2={hum}&field3={presion}&field4={calidad_aire}&field5={luz}"
    full_url = url + query_string

    try:
        response = urequests.get(full_url)
        print("Respuesta de ThingSpeak:", response.text)
        if response.status_code == 200:
            print("Datos enviados correctamente!")
        else:
            print(f"Error al enviar datos: {response.status_code}")
        response.close()
    except Exception as e:
        print("Error en la solicitud HTTP:", e)

# Configurar botón en pin 13 con resistencia pull-up
boton = Pin(13, Pin.IN, Pin.PULL_UP)

# Conexión WiFi
if conectaWifi("Wokwi-GUEST", ""):
    print("¡Conexión exitosa!")
    print("Datos de red:", network.WLAN(network.STA_IF).ifconfig())

    while True:
        # Verificar si se presiona el botón (LOW)
        if boton.value() == 0:
            print("Botón presionado. Enviando datos...")
            # Simulación de sensores
            temp = random.randint(18, 30)
            hum = random.randint(40, 60)
            presion = random.randint(1010, 1025)
            calidad_aire = random.randint(0, 500)
            luz = random.randint(100, 1000)
            
            print("T={:02d} °C, H={:02d} %, P={:03d} hPa, CA={:03d} ppm, L={:03d} lux".format(temp, hum, presion, calidad_aire, luz))
            enviarDatos(temp, hum, presion, calidad_aire, luz)
            
            # Esperar a que se suelte el botón para evitar múltiples envíos
            while boton.value() == 0:
                time.sleep(0.1)
        time.sleep(0.1)  # Evita alto consumo de CPU

else:
    print("¡Imposible conectar!")
    network.WLAN(network.STA_IF).active(False)
