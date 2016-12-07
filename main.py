from lifxlan import*
import sys, math, datetime
import serial, string, os
import RPi.GPIO as GPIO
import time
import serial
import io
import subprocess
from subprocess import check_output
from time import sleep
from methods import *
import thread
import pygame

'''
This script is responsible for all immediate functionality of the controller
and for connecting it to all modules (projector, bulb, sound).

2 = on/off light
3 = light toggle
4 = projection next
17 = projection toggle
27 = projection back
'''
pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
lumos_pid = os.getpid()

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP) # on/off state of bulb
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP) # light toggle: 1 = manual, 0 = day/night
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP) # projector forward
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) # projector/sendlove toggle: 1 = projector, 0 = sendLove
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # projector backward

ser = serial.Serial('/dev/ttyACM0', 9600) # for reading serial from redbear duo

# environment init
projector_toggle = 0 # 0 = rain, 1 = forest, 2 = creek, 3 = fire, 4 = brown noise
send_love_on = 0
num_env = 4

# values for bulb when it's first turned on
default_c = 0
default_s = 0
default_b = 65535
default_k = 9000

# bulb init
color_tolerance = 500
bulb_tolerance = 1000

prev_color = 0
prev_brightness = 0
prev_kelvin = 0

bulb_m = 16.38375
bulb_b = 819.1875
bulb_max_converted = 65535

kelvin_m = 1.625
kelvin_b = 2418.75
kelvin_min_converted = 2500
kelvin_max_converted = 9000
kelvin_tolerance = 200 # no idea if this is correct
man_kelvin = 2500

man_saturation = 65535

# sound init
mpdport = "6600"
noise_tolerance = 2
prev_noise = 100
noise_m = 0.025
noise_b = 1.25
noise_max_converted = 100

# url information
send_love_url = 'https://lumoslight.000webhostapp.com/orig/slideshow.php'
sound_dict = {0:'light_rain.mp3', 1:'winter_solstice_night.mp3', 2:'evening_lake.mp3', 3:'hearth.mp3'}
visual_dict = {0:'hello_rain.h264', 1:'winter_solstice.h264', 2:'evening_lake.h264', 3:'hello_hearth.h264'}
# light_dict = {0:[22755, 39321, 32767, 2500], 1:[39321, 9830, 32767, 2500], 2: [7827, 52428, 32767, 2500], 3: [31129, 39321, 32767, 2500], 4: [44964, 65535, 32767, 2500]}

# SET UP COMMANDS ==================================================================
# start mpc
os.system('mpc update')
os.system('mpc -p 6600')
os.system('mpc repeat on')
os.system('mpc play')
os.system('mpc crossfade 10') # not sure how much difference this makes

curr_pid = -1
nightday_pid = -1

prev_env_mail_toggle = -1
prev_bulb_onoff = -1
prev_bulb_mode = -1
day_night_pid = -1

# set up bulb
lifxlan = LifxLAN()
while True:
	if prev_env_mail_toggle:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				pygame.quit()
				os.system('mpc clear')
				os.system('mpc stop')
				# print("killing pid = " + str(curr_pid))
				os.system('kill -9 ' + curr_pid)
				exit()
	try:
		msg = ser.readline()
		while len(str(msg)) == 1:
			# print("No information from redbear. Waiting.")
			time.sleep(5)
		noise_pot, color_pot, brightness_pot, kelvin_pot = get_pot_values(msg)

		# turn serial information into useful information
		volume, prev_noise = convert_raw_bulb_info(noise_pot, prev_noise, noise_tolerance, noise_m, noise_b, noise_max_converted)
		color, prev_color = convert_raw_bulb_info(color_pot, prev_color, color_tolerance, bulb_m, bulb_b, bulb_max_converted)
		brightness, prev_brightness = convert_raw_bulb_info(brightness_pot, prev_brightness, bulb_tolerance, bulb_m, bulb_b, bulb_max_converted, bulb_on)

		os.system('mpc volume ' + str(volume))

		# BUTTONS: assign button inputs to variables
		bulb_onoff = GPIO.input(2) # 1 = on; 0 = off; HELD STATE TOGGLE
		bulb_mode = GPIO.input(3) # 1 = manual, 0 = day/night; HELD STATE TOGGLE
		projector_forward = GPIO.input(4)
		projector_backward = GPIO.input(27)
		env_mail_toggle = GPIO.input(17) # 1 = projection; 0 = mail; HELD STATE TOGGLE

		# How each button causes the device to respond: ========================
		# 1. If on/off has changed, deal with it
		if prev_bulb_onoff == -1 or prev_bulb_onoff != bulb_onoff:
			prev_bulb_onoff = bulb_onoff
			if bulb_onoff:
				bulb_on(lifxlan, default_c, default_s, default_b, default_k)
			else:
				bulb_off(lifxlan)

		# 2. If env_mail_toggle has changed, deal with it
		if (prev_env_mail_toggle == -1) or (prev_env_mail_toggle != env_mail_toggle):
			prev_env_mail_toggle = env_mail_toggle
			if env_mail_toggle == 0:
				curr_pid = display_postcards(curr_pid, send_love_url)
			else:
				curr_pid = display_env(projector_toggle, visual_dict, sound_dict, curr_pid)

		# 3. If bulb_mode has changed, deal with it
		if prev_bulb_mode == -1 or prev_bulb_mode != bulb_mode:
			prev_bulb_mode = bulb_mode
			if bulb_mode: # manual
				if nightday_pid != -1 and nightday_pid != lumos_pid:
					os.system('kill -9 ' + nightday_pid)
					nightday_pid = -1
				bulb_on(lifxlan, color, man_saturation, brightness, man_kelvin)
			else: # automatic day-night reflection
				os.system('python fullday_simulation.py &')
				nightday_pid = check_output(["pidof", "python"]).strip('\n').split(' ')
				nightday_pid = nightday_pid[0]

		if bulb_mode and bulb_onoff:
			bulb_on(lifxlan, color, man_saturation, brightness, man_kelvin)

		# 4. Environment toggling (forward and backward)
		if projector_forward == 0 and prev_env_mail_toggle:
			projector_toggle += 1
			projector_toggle = projector_toggle % num_env
			curr_pid = display_env(projector_toggle, visual_dict, sound_dict, curr_pid)

		if projector_backward == 0 and prev_env_mail_toggle:
			projector_toggle -= 1
			if projector_toggle == -1:
				projector_toggle = num_env - 1
			curr_pid = display_env(projector_toggle, visual_dict, sound_dict, curr_pid)

		time.sleep(0.1)
	except KeyboardInterrupt:
		pygame.display.quit()
		pygame.quit()
		os.system('mpc clear')
		os.system('mpc stop')
		# print("killing pid = " + str(curr_pid))
		os.system('kill -9 ' + curr_pid)
		exit()
