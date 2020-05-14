#!/usr/bin/python3
import smbus
import Adafruit_DHT
import time
import spidev
import RPi.GPIO as GPIO
from flask import Flask, render_template, request

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

# GPIO pins setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Create sensor object
DHT_sensor = Adafruit_DHT.DHT11
dht_pin = 16 # data pin on the raspberry pi

# global variables
humidity = 0
temperature = 0

# Define sensor channels
light_channel = 0
temp_channel  = 1

# Water pump GPIO
pump = 23
#initialize water pump status
pumpSts = 0
# define as output and turn off
GPIO.setup(pump, GPIO.OUT)
GPIO.output(pump, GPIO.LOW)

def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def ConvertTemp(data):

  # ADC Value
  # (approx)  Temp  Volts
  #    0      -50    0.00
  #   78      -25    0.25
  #  155        0    0.50
  #  233       25    0.75
  #  310       50    1.00
  #  465      100    1.50
  #  775      200    2.50
  # 1023      280    3.30

  temp = ((data * 330)/float(1023))-50
  temp = round(temp,2)
  return temp


app = Flask(__name__)

@app.route('/') # this tells the program what url triggers the function when a request is made
def index():

#    global temperature, humidity

    try: #check to see if the DHT sensor is connected
        humidity, temperature = Adafruit_DHT.read_retry(DHT_sensor, dht_pin) #get the values from the sensor
        if humidity is not None and temperature is not None:
            tVal = '{:.1f}'.format(temperature)
            hVal = '{:.1f}'.format(humidity)
        humidity ='{:.1f}'.format(humidity)         #convert value to one decimal place
        temperature ='{:.1f}'.format(temperature)   #convert value to one decimal place
    except: # If the sensor is not connected send null  values
        humidity = 0
        temperature = 0
        pass

    try:
        # Read the light sensor data
        light_level = ReadChannel(light_channel)
    except: # If the sensor is not connected send null values
        light_level = 0
        pass

    try:
        # Read the temperature sensor data
        temp_level = ReadChannel(temp_channel)
        temp = ConvertTemp(temp_level)
    except:
        temp = 0
        pass

    try:
        # Read water pump status
        pumpSts = GPIO.input(pump)
    except:
        pumpSts = 0
        pass


    #variables to pass through to the web page
    templateData = {
            'title': 'Smart Garden',
            'humidity' : humidity,
            'temperature' : temperature,
            'light' : light_level,
            'temp' : temp
#            'pump': pumpSts
    }
    return render_template('index.html', **templateData) #when a html request has been made return these values

@app.route("/<deviceName>/<action>")
def action(deviceName, action):

        if action == "on":
                GPIO.output(pump, GPIO.HIGH)
        if action == "off":
                GPIO.output(pump, GPIO.LOW)

        pumpSts = GPIO.input(pump)

        templateData = {
              'temperature': temperature,
              'humidity': humidity,
              'pump'  : pumpSts
        }
        return render_template('index.html', **templateData)


if __name__ == '__main__':
        app.jinja_env.cache = {}
        app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

