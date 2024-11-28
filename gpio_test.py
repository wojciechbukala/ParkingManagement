import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
outpin = 21
GPIO.setup(outpin, GPIO.OUT)
#GPIO.output(outpin, GPIO.HIGH) 
while True:
    GPIO.output(outpin, GPIO.HIGH) 
    time.sleep(5)
    GPIO.output(outpin, GPIO.LOW) 
    time.sleep(5)
