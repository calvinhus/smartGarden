import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta, timezone
from suntime import Sun
import pytz
import IPMA

# PIN connected to water pump
bomba = 23

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(bomba,GPIO.OUT)

# coordenadas Covilhã
latitude = 40.28
longitude = -7.50
utc = pytz.utc

sun = Sun(latitude, longitude)

nascerSol = sun.get_sunrise_time()
porSol =  sun.get_sunset_time()

#horario de verao
now = datetime.now().replace(tzinfo=utc)
dia = now.day
mes = now.month
hoje = (mes, dia)
iniVerao = (3, 29)
fimVerao = (10, 25)

if iniVerao < hoje < fimVerao:
    nascerSol = nascerSol + timedelta(hours=1)
    porSol = porSol + timedelta(hours=1)


print("Agora: ", str(now))
print("Nascer hoje: ", str(nascerSol))
print("Por hoje: ", str(porSol))

fakeSunRise = now + timedelta(minutes=10)
print("nascer fake: " , str(fakeSunRise))

#chuva, tMn, tMx = (IPMA.chamadaAPI(0))
#print("-------Hoje-------")
#print('Chuva: {} \nTmin: {}\nTmax: {}\n'.format(chuva, tMn, tMx))

#chuva, tMn, tMx = (IPMA.chamadaAPI(1))
#print("-------Amanha-------")
#print('Chuva: {} \nTmin: {}\nTmax: {}\n'.format(chuva, tMn, tMx))

chuva, tMn, tMx = (IPMA.chamadaAPI(2))
print("-------DepoisAmanha-------")
print('Chuva: {} \nTmin: {}\nTmax: {}\n'.format(chuva, tMn, tMx))
if chuva >= 2:
	print("chhhhhhh")

GPIO.cleanup()
'''
try:
        while True:
                now = datetime.now().replace(tzinfo=utc)
                if now >= fakeSunRise:
                        #set high
                        print ("Setting high - PUMP ON")
                        GPIO.output (bomba, GPIO.HIGH)
                        time.sleep(2)
                else:
                        pass

except KeyboardInterrupt:
        GPIO.cleanup()
        print ("Bye")

'''
