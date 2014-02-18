import os
import sys
import glob
import time
import logging
import smtplib
from datetime import datetime
import RPi.GPIO as GPIO
#path for log location
sys.path.append("/home/pi")
#gpioPin for matt 1
MatPinValve1 = 17
GPIO.cleanup(MatPinValve1)
GPIO.setwarnings(False)
#global g_mat_status
g_mat_status = 'unkown, has not been set'
g_msg_for_email = 'empty msg'
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
 
def sendemail(from_addr, to_addr_list, 
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    #header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()



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
def matPinStatus():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MatPinValve1,GPIO.OUT)
    GPIO.setwarnings(False) #supress warning
    MatGPIO_Pin_stat = GPIO.input(MatPinValve1)
    global g_mat_status
    if MatGPIO_Pin_stat == 0:
    	msg = 'mat pin reports LOW or ON'
	#print(msg)
        g_mat_status = 'on'
	return msg
    elif MatGPIO_Pin_stat == 1:
    	msg = 'mat pin reports HIGH or OFF'
	g_mat_status = 'off'
        #print(msg)
        return msg
    else:
    	msg = 'mat pin reporter error'
        #print(msg)
        return msg
 


def matControl():
    global g_mat_status
    global g_msg_for_email 
    mat_status = g_mat_status 
    #return status
    bedTemp = read_temp2()
    msg = 'Mat control main loop pre run........Seed soil temp1: ' + str(bedTemp) + ' Bed Hi Temp: ' + str(bedHiTemp) + ' Bed Low Temp: ' + str(bedLowTemp) + ' Mat Status: ' + mat_status
    g_msg_for_email = msg
    print msg 
    #print bedTemp, bedHiTemp, bedLowTemp
    if bedTemp > bedHiTemp:
        #logging.warning('temp over:',bedTemp)
        logging.info('temp over triggered Mat 1 OFF') 
        #set bed gpio off
	if mat_status <> 'off':
        	logging.info('Mat 1 stopping now')
        	GPIO.setmode(GPIO.BCM) #numbering scheme that corresponds to breakout board$
        	GPIO.setwarnings(False) #supress warning
        	GPIO.setup(MatPinValve1,GPIO.OUT) #replace pinNum with whatever pin you used, th$ 
        	GPIO.output(MatPinValve1,GPIO.HIGH)
	
	logging.info('Mat1 OFF')
        #future lights below 
	g_mat_status = 'off'
	mat_status = 'off'
	#Mat_LastSet = 'off'
        logging.info('Mat off cycle exiting')
        #log messages
        return mat_status
    elif bedTemp < bedLowTemp:
        #logging.warning('temp under:',bedTemp)
        logging.info('temp under triggered Mat 1 on')     
        
	if mat_status <> 'on':
		logging.info('Mat 1 starting now')
        	GPIO.setmode(GPIO.BCM) #numbering scheme that corresponds to breakout board$
        	GPIO.setwarnings(False) #supress warning
        	GPIO.setup(MatPinValve1,GPIO.OUT) #replace pinNum with whatever pin you used, th$ 
        	GPIO.output(MatPinValve1,GPIO.LOW)
        
	logging.info('Mat1 ON')
        #future lights below
	g_mat_status = 'on'
        mat_status = 'on'
        #Mat_LastSet = 'on'
        logging.info('Mat on cycle exiting')
        return mat_status
    else:
        logging.info('seed temp in range exiting') 
        #mat_status = mat_status
	#mat_status = 'unkown'
	#print(g_mat_status)
	return mat_status
while True:
    localtime = time.asctime( time.localtime(time.time()) )
    print "Local current time: ", localtime
    print "Mat Pin Status: " + matPinStatus()
    print "Green House: " + str(read_temp())
    logging.info(read_temp())
    print "Soil Bed: " + str(read_temp2())
    logging.info(read_temp2())
    print "Room: " + str(read_temp3())  
    logging.info(read_temp3())
    print "Mat status"
    print('Mat:' + matControl())
    # sendemail(from_addr    = 'xyz@gmail.com', 
    #       to_addr_list = ['xyz@gmail.com'],
    #       subject      = 'BedStatus', 
    #       message      = g_msg_for_email, 
    #       login        = 'login', 
    #       password     = 'password')
    #print(matPinStatus())
    #logging(mattControl())
    time.sleep(60)


