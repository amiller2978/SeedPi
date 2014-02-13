import sys
sys.path.append("/home/pi")
import time
# import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep
import RPi.GPIO as GPIO
#!!!!!!!!!!configs!!!!!!!!!!

#time in seconds that the valve will run for
#vavle1time = 400
#vavle2time = 500
#Pins used on GPIO 
pinValve1 = 22
import logging
logging.basicConfig(filename='/home/pi/light_status.log',level=logging.DEBUG,format='%(asctime)s %(message)s')
logging.info('light off cycle starting')
#logging.warning('And this, too')

GPIO.setmode(GPIO.BCM) #numbering scheme that corresponds to breakout board$

#turn on gpio, log start, sleep for time, turn gpio off, logg off
logging.info('Light 1 stopping now')
GPIO.setmode(GPIO.BCM) #numbering scheme that corresponds to breakout board$
GPIO.setup(pinValve1,GPIO.OUT) #replace pinNum with whatever pin you used, th$ 
GPIO.output(pinValve1,GPIO.HIGH)
logging.info('Light1 OFF')
#future lights below
logging.info('Light off cycle exiting')
