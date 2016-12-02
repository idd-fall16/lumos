from lifxlan import*
import sys, math, pyowm, datetime
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
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # on/off state of bulb
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP) # projector toggle
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) # goes directly to sendLove

ser = serial.Serial('/dev/ttyACM0', 9600) # for reading serial from redbear duo

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

# bulb init
is_manual = 1
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

saturation = 65535

# url information
send_love_url = 'https://lumoslight.000webhostapp.com/orig/slideshow.php'
sound_dict = {0:'light_rain.mp3', 1:'winter_solstice_night.mp3', 2:'diamond_peak_stream.mp3', 3:'hearth.mp3', 4:'brown_noise_short.mp3'}
visual_dict = {0:'hello_rain.h264', 1:'winter_solstice.h264', 2:'hello_cascade.h264', 3:'hello_hearth.h264', 4:'brown_sky.h264'}

# SET UP COMMANDS ==================================================================
# start mpc
os.system('mpc update')
os.system('mpc -p 6600')
os.system('mpc add ' + sound_dict[projector_toggle])
os.system('mpc play')
os.system('mpc crossfade 10') # not sure how much difference this makes

# open chromium
# os.system('chromium-browser --kiosk ' + visual_dict[projector_toggle] + ' --incognito &') # alt+f4 to escape

# start video
os.system('./hello_video.bin ' + visual_dict[projector_toggle] + ' &')
curr_pid = get_pid()

# set up bulb
lifxlan = LifxLAN()
time.sleep(5)
while True:
	try:
		# read from serial
		msg = ser.readline()

		noise_index = msg.find("N")
		color_index= msg.find("C")
		brightness_index = msg.find("B")
		kelvin_index = msg.find("K")

		noise_pot_value = msg[noise_index+1:]
		color_pot_value = msg[color_index+1:brightness_index]
		brightness_pot_value = msg[brightness_index+1:kelvin_index]
		kelvin_pot_value = msg[kelvin_index+1:noise_index]

		print("noise_pot_value = " + str(noise_pot_value))

		# gpio info
		bulb_on = True #TODO comment this out and use line below
		# bulb_on = GPIO.input(27) # if this is 0 then set to true
		bulb_state = GPIO.input(17)
		projector_toggle_state = GPIO.input(22) # controls environment visuals
		send_love_state = GPIO.input(23) # controls what the user sees
		print("activate 24 hour simulation state = " + str(bulb_state))
		print("projector_toggle_state = " + str(projector_toggle_state))

		# turn serial information into useful information
		volume, prev_noise = convert_raw_bulb_info(noise_pot_value, prev_noise, noise_tolerance, noise_m, noise_b, noise_max_converted)
		color, prev_color = convert_raw_bulb_info(color_pot_value, prev_color, color_tolerance, bulb_m, bulb_b, bulb_max_converted)
		brightness, prev_brightness = convert_raw_bulb_info(brightness_pot_value, prev_brightness, bulb_tolerance, bulb_m, bulb_b, bulb_max_converted, bulb_on)
		# kelvin, prev_kelvin = convert_raw_bulb_info(kelvin_pot_value, prev_kelvin, kelvin_tolerance, kelvin_m, kelvin_b, kelvin_max_converted, 1, kelvin_min_converted)
		kelvin = 2500

		print("volume = " + str(volume))
		print("color = " + str(color))
		print("brightness = " + str(brightness))

		# respond to collected info
		os.system('mpc volume ' + str(volume))

		# Send updated parameter to LIFX Bulb
		if is_manual and bulb_state:
			bulb_settings = [color, saturation, brightness, kelvin];
			lifxlan.set_color_all_lights(bulb_settings, rapid=True)
		elif is_manual and bulb_state == 0:
			# if bulb_state == 0: # switch is default 1
			print("light simulation")
			os.system('python ~/Desktop/automatic_full_day_simulation.py &')
		# else:
			# won't happen on monday
			# for non-manual mode

		if projector_toggle_state == 0:
			if send_love_on == 1:
				print("killing pid = " + str(curr_pid))
				os.system('kill -9 ' + curr_pid + " &")
				curr_pid = get_pid()
				send_love_on = 0

			projector_toggle += 1
			projector_toggle = projector_toggle % num_env

			# open up new video
			os.system('./hello_video.bin ' + visual_dict[projector_toggle] + ' &')

			print("killing pid = " + str(curr_pid))
			os.system('kill -9 ' + curr_pid + " &")
			curr_pid = get_pid()

			# os.system('chromium-browser --kiosk ' + visual_dict[projector_toggle] + ' --incognito &') # alt+f4 to escape
			# os.system('xdotool search --onlyvisible --class "chromium" windowfocus and xdotool type ' + visual_dict[projector_toggle] + ' and xdotool key Return')
			os.system('mpc add ' + sound_dict[projector_toggle])
			os.system('mpc next') # force next
			os.system('mpc crop') # get rid of previous track

		if send_love_state == 0:
			print("send_love_state = " + str(send_love_state))
			if send_love_on == 0:
				print("opening send love")
				os.system('chromium-browser --kiosk ' + send_love_url + ' &') # alt+f4 to escape
				# os.system('@chromium --kiosk ' + send_love_url)
				send_love_on = 1

				# stop sound
				os.system('mpc clear')

				# kill video
				print("turning on slideshow")
				print("killing pid = " + str(curr_pid))
				os.system('kill -9 ' + curr_pid + " &")

				time.sleep(5)

				# get pid of chrome process
				pids = check_output(["pidof", "chromium-browse"]).strip('\n').split(' ')
				curr_pid = pids[len(pids) - 1]
				print("chrome pid = " + str(curr_pid))

			else:
				# os.system('chromium-browser --kiosk ' + visual_dict[projector_toggle] + ' &') # alt+f4 to escape
				send_love_on = 0

				# open up new video
				# os.system('./hello_video.bin ' + visual_dict[projector_toggle] + ' &')

				print("Turning off slideshow: killing pid = " + str(curr_pid))
				os.system('kill -9 ' + curr_pid + " &")

				os.system('./hello_video.bin ' + visual_dict[projector_toggle] + ' &')

				curr_pid = get_pid()

				# os.system('chromium-browser --kiosk ' + visual_dict[projector_toggle] + ' --incognito &') # alt+f4 to escape
				# os.system('xdotool search --onlyvisible --class "chromium" windowfocus and xdotool type ' + visual_dict[projector_toggle] + ' and xdotool key Return')
				os.system('mpc add ' + sound_dict[projector_toggle])
				os.system('mpc play')
				time.sleep(3)

		time.sleep(0.1)
	except KeyboardInterrupt:
		os.system('mpc clear')
		os.system('mpc stop')
		print("killing pid = " + str(curr_pid))
		os.system('kill -9 ' + curr_pid)
		exit()
