# Author:Rucha Chauthai
# DS18B20 digital temperature sensor with raspberry pi

#Activate 1-wire protocol from 
#Raspberry menu -> preferences -> Raspberry pi configuration -> interfaces -> 1-wire=Enable

#pin connections
#VCC -> 3.3
#GND -> 0V
#data ->pin-7

import os											#OS library for terminal functions
import glob											#file handling library in python
import time											#time-keeping library
 
os.system('modprobe w1-gpio')						#probe kernel module for 1 wire device
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'					#base directory for one wire devices
device_folder = glob.glob(base_dir + '28*')[0]		#looks for device address startng with 28-
device_file = device_folder + '/w1_slave'			#add w1_slave file name in final path
 
def read_temp_raw():								#read device-file for temperature
    f = open(device_file, 'r')						#open file in read mode
    lines = f.readlines()							#read all lines form file
    f.close()										#closes open file buffer
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':			#checksum shoud return yes for non-corrupt data
        time.sleep(0.2)
        lines = read_temp_raw()

    equals_pos = lines[1].find('t=')				#finds "t=" in the line number 2
    if equals_pos != -1:							#if found, then picks up dataout of it
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0		#conversion to degrees
        temp_f = temp_c * 9.0 / 5.0 + 32.0			#conversion to fahrenheits
        return temp_c, temp_f
	
while True:

	print(read_temp())								#print temp with delay of 1 second
	time.sleep(1)
	