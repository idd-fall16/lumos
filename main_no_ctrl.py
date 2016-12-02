# from lifxlan import*
import sys, math, datetime
import serial, string, os
import RPi.GPIO as GPIO
import time
import serial
import io
import subprocess
from subprocess import check_output
from time import sleep
from bulb_methods import *
'''
This script is responsible for all immediate functionality of the controller
and for connecting it to all modules (projector, bulb, sound).

2 = on/off light 
3 = light toggle
4 = projection next
17 = projection toggle
27 = projection back
'''

def getkey():
	fd = sys.stdin.fileno()
	old = termios.tcgetattr(fd)
	new = termios.tcgetattr(fd)
	new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
	new[6][TERMIOS.VMIN] = 1
	new[6][TERMIOS.VTIME] = 0
	termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
	c = None
	try:
		c = os.read(fd, 1)
	finally:
		termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
	return c

def get_pid():
	return check_output(["pidof", "hello_video.bin"]).strip('\n')

GPIO.setmode(GPIO.BCM)
# GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP) # on/off state of bulb
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP) # light toggle: 1 = manual, 0 = day/night
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP) # projector forward
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) # projector/sendlove toggle: 1 = projector, 0 = sendLove
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # projector backward

# environment init
projector_toggle = 0 # 0 = rain, 1 = forest, 2 = creek, 3 = fire, 4 = brown noise
send_love_on = 0
num_env = 5

# sound init
mpdport = "6600"
noise_tolerance = 2
prev_noise = 100
noise_m = 0.025
noise_b = 1.25
noise_max_converted = 100

# url information
send_love_url = 'https://lumoslight.000webhostapp.com/orig/slideshow.php'
sound_dict = {0:'light_rain.mp3', 1:'winter_solstice_night.mp3', 2:'diamond_peak_stream.mp3', 3:'hearth.mp3', 4:'brown_noise_short.mp3'}
visual_dict = {0:'hello_rain.h264', 1:'winter_solstice.h264', 2:'hello_cascade.h264', 3:'hello_hearth.h264', 4:'brown_sky.h264'}

# SET UP COMMANDS ==================================================================
# start mpc
os.system('mpc update')
os.system('mpc -p 6600')
os.system('mpc repeat on')
os.system('mpc add ' + sound_dict[projector_toggle])
os.system('mpc play')
os.system('mpc crossfade 10') # not sure how much difference this makes

# start video
os.system('./hello_video.bin ' + visual_dict[projector_toggle] + ' &')
curr_pid = get_pid()
prev_send_love_state = -1

# set up bulb
# lifxlan = LifxLAN()
time.sleep(5)
while True:
	try:
		bulb_onoff = GPIO.input(2) # 1 = on; 0 = off
		light_mode 
		projector_toggle_state = GPIO.input(4) # controls environment visuals; officially 4
		send_love_state = GPIO.input(17) # controls what the user sees; toggle switch (1 = projection; 0 = mail); officially 17
		if prev_send_love_state == -1:
			prev_send_love_state = send_love_state

		if projector_toggle_state == 0 and prev_send_love_state == 1: # projector toggle was pressed, user wants next video
			projector_toggle += 1
			projector_toggle = projector_toggle % num_env

			# open up new video
			os.system('./hello_video.bin ' + visual_dict[projector_toggle] + ' &')

			print("killing pid = " + str(curr_pid))
			os.system('kill -9 ' + curr_pid + " &")
			curr_pid = get_pid()

			os.system('mpc add ' + sound_dict[projector_toggle])
			os.system('mpc next') # force next
			os.system('mpc crop') # get rid of previous track

		if send_love_state != prev_send_love_state:
			print("send_love_state = " + str(send_love_state))
			print("prev_send_love_state = " + str(prev_send_love_state))
			prev_send_love_state = send_love_state

			if send_love_state == 0: # mail
				# kill video
				print("turning on slideshow")
				print("killing pid = " + str(curr_pid))
				os.system('kill -9 ' + curr_pid + " &")
			
				os.system('sudo -u pi chromium-browser --kiosk ' + send_love_url + ' &') # alt+f4 to escape

				time.sleep(3)

				# stop sound
				os.system('mpc clear')

				# get pid of chrome process
				pids = check_output(["pidof", "chromium-browse"]).strip('\n').split(' ')
				curr_pid = pids[len(pids) - 1]
				print("chrome pid = " + str(curr_pid))

			else: # projection
				# kill chrome slideshow
				print("Turning off slideshow: killing pid = " + str(curr_pid))
				os.system('kill -9 ' + curr_pid + " &")
				time.sleep(1)

				# open up new video
				os.system('./hello_video.bin ' + visual_dict[projector_toggle] + ' &')
				os.system('mpc add ' + sound_dict[projector_toggle])
				os.system('mpc play')

				# get video pid
				curr_pid = get_pid()

		time.sleep(0.1)
	except KeyboardInterrupt:
		os.system('mpc clear')
		os.system('mpc stop')
		print("killing pid = " + str(curr_pid))
		os.system('kill -9 ' + curr_pid)
		exit()
