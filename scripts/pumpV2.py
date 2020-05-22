import RPi.GPIO as GPIO
import time
import IPMA

# PIN connected to water pump
bomba = 23

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(bomba,GPIO.OUT)

chuva, tMn, tMx = (IPMA.chamadaAPI(2))
print("-------DepoisAmanha-------")
print('Chuva: {} \nTmin: {}\nTmax: {}\n'.format(chuva, tMn, tMx))

# Dia: 0 - Hoje | 1 - Amanhã | 2 - Depois de amanhã
dia = 0
rega = 60 # regar 1 min
try:
    chuva, tMn, tMx = (IPMA.chamadaAPI(dia))
    if chuva >= 50:
        print("Vai chover hoje. Rega cancelada.")
    else:
        print("A regar {} segundos".format(rega))
        GPIO.output (bomba, GPIO.HIGH)
        time.sleep(rega)
        GPIO.output (bomba, GPIO.LOW)
        GPIO.cleanup()

except KeyboardInterrupt:
    GPIO.cleanup()
    print ("Bye")

