import os
import sys
import glob
import time
import logging
from datetime import datetime
import RPi.GPIO as GPIO
#path for log location
sys.path.append("/home/pi")
#gpioPin for matt 1
MattPinValve1 = 22 

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

bedAlarmHiTemp = 92
bedHiTemp = 85
bedLowTemp= 75
bedAlarmLowTemp = 70
base_dir = '/sys/bus/w1/devices/'
#devices on seedPi 28-000003b6f897- room 28-000005b38e21  28-000005b3e077 
device_folder = glob.glob(base_dir + '28-000005b3e0*')[0]
device_file = device_folder + '/w1_slave'

device_folder2 = glob.glob(base_dir + '28-000005b38e*')[0]
device_file2 = device_folder2 + '/w1_slave'

device_folder3 = glob.glob(base_dir + '28-000003b*')[0]
device_file3 = device_folder3 + '/w1_slave'
logging.basicConfig(filename='/home/pi/seedtemp.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

logging.info('Temp logging starting')
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp_raw2():
    f = open(device_file2, 'r')
    lines = f.readlines()
    f.close()
    return lines
def read_temp_raw3():
    f = open(device_file3, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

def read_temp2():
    lines = read_temp_raw2()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw2()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

def read_temp3():
    lines = read_temp_raw3()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw3()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

def mattControl():
    matt_staus = 'unset'
    #return status
    bedTemp = read_temp2()
    print 'Seed soil temp1:', bedTemp, bedHiTemp, bedLowTemp
    if bedTemp > bedHiTemp:
        logging.warning('temp over: %S',bedTemp)
        logging.info('temp over triggered matt 1 OFF') 
        #set bed gpio off
        logging.info('matt 1 stopping now')
        GPIO.setmode(GPIO.BCM) #numbering scheme that corresponds to breakout board$
        GPIO.setwarnings(False) #supress warning
        GPIO.setup(MattPinValve1,GPIO.OUT) #replace pinNum with whatever pin you used, th$ 
        GPIO.output(MattPinValve1,GPIO.HIGH)
        logging.info('Matt1 OFF')
        #future lights below
        matt_staus = 'off'
        logging.info('Matt off cycle exiting')
        #log messages
        return matt_staus
    elif bedTemp < bedLowTemp:
        logging.warning('temp under: %S',bedTemp)
        logging.info('temp under triggered matt 1 on')     
        logging.info('matt 1 starting now')
        GPIO.setmode(GPIO.BCM) #numbering scheme that corresponds to breakout board$
        GPIO.setwarnings(False) #supress warning
        GPIO.setup(MattPinValve1,GPIO.OUT) #replace pinNum with whatever pin you used, th$ 
        GPIO.output(MattPinValve1,GPIO.LOW)
        logging.info('Matt1 ON')
        #future lights below
        matt_staus = 'on'
        logging.info('Matt on cycle exiting')
        return matt_staus
while True:
    localtime = time.asctime( time.localtime(time.time()) )
    print "Local current time :", localtime
    print "Room"
    print(read_temp())
    logging.info(read_temp())
    print(read_temp2())	
    logging.info(read_temp2())
    
    print(read_temp3())  
    logging.info(read_temp3())
    print(mattControl())
    #logging(mattControl())
    time.sleep(60)
