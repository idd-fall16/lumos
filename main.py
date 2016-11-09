import serial, string, os
import RPi.GPIO as GPIO
import time
import serial
import os
from time import sleep
'''
This script is responsible for all immediate functionality of the controller
and for connecting it to all modules (projector, bulb, sound).
'''

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#ser = serial.Serial('/dev/ttyACM0', 9600) # for reading serial from redbear duo

while True:
    try:

        noise_state = GPIO.input(27)
        bulb_state = GPIO.input(17)
        if noise_state == 0:
            os.system('mpg123 -q slowly-raining-loop.mp3 &')
        if bulb_state == 0: # switch is default 1
            os.system('python ~/Desktop/fullday_simulation.py &')
        time.sleep(0.05)

        '''
        if ((not prev_input) and input):
            print("button pressed")
        prev_input = input
        '''

        '''
        msg = ser.readline()
        print(str(msg))
	if "button pressed" in str(msg):
		os.system('mpg123 -q slowly-raining-loop.mp3 &')
        time.sleep(0.05)
        '''
    except KeyboardInterrupt:
        exit()
