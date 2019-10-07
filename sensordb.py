#JHON BAYRON PEREZ 
#   instalar pip3 :
#          - sudo apt-get update
#          - sudo apt-get install python3-pip
#          - sudo python3 -m pip install --upgrade pip setuptools wheel

# Instalamos la libreria de firebase en real time,rpi.gpio,adafruit_DTH11,urllib2
#sudo apt-get install rpi.gpio - o tambien - pip3 install RPi.GPIO
#sudo pip3 install Adafruit_DHT

# Importamos la libreria de firebase
from firebase import firebase
# Importamos la libreria para mirar la fecha y hora.
import datetime
# importamos la libreria de Entradas y salidas
import RPi.GPIO as GPIO
# importamos libreria para aplicar tiempo de espera.
from time import sleep
# Importamos libreria adafruit
import Adafruit_DHT

import json
import os
from functools import partial

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setwarnings(False)

# Creamos una variable para guardar la extension de la libreria adafruit
sensor = Adafruit_DHT.DHT11

# Conexion al pin 8-GPIO14.
pin = 14

#Creamos la base de datos y pasamos el link de donde esta alojada (este caso FIREBASE )
url = 'https://nombre_proyecto.firebaseio.com/'
db = firebase.FirebaseApplication('{}'.format(url),None)


def subir_firebase(db):

    humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)

    if humedad is not None and temperatura is not None:
    	sleep(3)
        #Convertimos a Celcius  y a humedad
    	str_temp = ' {0:0.2f} *C '.format(temperatura)
    	str_hum  = ' {0:0.2f} %'.format(humedad)

        #Imprimame la humedad y temperatura en la consola
    	print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(str_temp, str_hum))

    else:
    	print('Fallo la lectura, Intente de nuevo!')
    	sleep(5)

	# Creamos una variable para guardar el formato fecha y hora
    fechaActual = datetime.datetime.now()
    horaIO = ("%s:%s:%s"%(fechaActual.hour,fechaActual.minute,fechaActual.second))
    fechaIO = ("%s-%s-%s" %(fechaActual.year, fechaActual.month, fechaActual.day))

    # Formato json y subimos los datos a firebase
    data = {
        "hora":horaIO,
        "fecha":fechaIO,
        "temp": temperatura,
        "humidity": humedad
        }
    db.post('/sensor/dht', data)

while True:
    subir_firebase(db)
    sleep(3)
