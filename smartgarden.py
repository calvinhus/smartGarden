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

DHT22_sensor = Adafruit_DHT.DHT22

pin = 4 #DHT22 data pin on the raspberry pi

# GPIO pins setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define sensor channels
light_channel = 0
temp_channel  = 1

#define water pump GPIO | using a LED for testing purposes
led = 23
#initialize water pump status
ledSts = 0
# define as output and turn off
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, GPIO.LOW)

def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def ConvertTemp(data,places):

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
  temp = round(temp,places)
  return temp


app = Flask(__name__)

@app.route('/') # this tells the program what url triggers the function when a request is made
def index():

    try: #check to see if the DHT sensor is connected
        humidity, temperature = Adafruit_DHT.read(DHT22_sensor, pin) #get the values from the sensor
        humidity ='{:.2f}'.format(humidity) #convert value to two decimal places
        temperature ='{:.1f}'.format(temperature) #convert value to one decimal place
        print(temperature)
        print("somethig")
    except: # If the sensor is not connected send null values
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
         temp = ConvertTemp(temp_level,2)
    except:
        temp = 0
        pass

    try:
        # Read water pump status
        ledSts = GPIO.input(led)
    except:
        ledSts = 0
        pass


    #variables to pass through to the web page
    templateData = {
            'title': 'Smart Garden',
            'humidity' : humidity,
            'temperature' : temperature,
            'light' : light_level,
            'temp' : temp,
            'led': ledSts
    }
    return render_template('index.html', **templateData) #when a html request has been made return these values

@app.route("/<deviceName>/<action>")
def action(deviceName, action):
        #if deviceName == 'led':
        #        actuator = led

        if action == "on":
                GPIO.output(led, GPIO.HIGH)
        if action == "off":
                GPIO.output(led, GPIO.LOW)

        ledSts = GPIO.input(led)

        templateData = {
              'led'  : ledSts
        }
        return render_template('index.html', **templateData)


if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5000)


        #app.config['SERVER_NAME'] = 'myapp.local'
        #app.run(host=app.config['SERVER_NAME'], port=5000, debug=True)
