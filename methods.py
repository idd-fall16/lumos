from lifxlan import*
import sys, math, datetime
import serial, string, os
import time
import serial
import io
import subprocess
from subprocess import check_output
from time import sleep

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

# ENVIRONMENT RELATED METHODS ==================================================

def display_postcards(curr_pid, send_love_url):
	if curr_pid != -1:
		os.system('kill -9 ' + curr_pid + " &")

	os.system('sudo -u pi chromium-browser --kiosk ' + send_love_url + ' &') # alt+f4 to escape

	time.sleep(3) # give chrome some time to boot

	# stop sound
	os.system('mpc clear')

	# get pid of chrome process
	not_ready = 1
	while not_ready:
		# try:
		not_ready = 0
		pids = check_output(["pidof", "chromium-browse"]).strip('\n').split(' ')
		curr_pid = pids[len(pids) - 1]
		print("chrome pid = " + str(curr_pid))
		# except subprocess.CalledProcessError:
		# 	not_ready = 1

	return curr_pid

def display_env(projector_toggle, visual_dict, sound_dict, curr_pid):
	# open up new video
	os.system('./hello_video.bin ' + visual_dict[projector_toggle] + ' &')

	# kill chrome process
	if curr_pid != -1:
		os.system('kill -9 ' + curr_pid + " &")
	curr_pid = get_pid()

	os.system('mpc add ' + sound_dict[projector_toggle])
	os.system('mpc play')
	os.system('mpc next') # force next
	os.system('mpc crop') # get rid of previous track
	return curr_pid

# BULB RELATED METHODS ==================================================

def bulb_off(lifxlan):
	lifxlan.set_color_all_lights([0, 0, 0, 0], rapid=True)

def bulb_on(lifxlan, c, s, b, k):
	default = [c, s, b, k]
	lifxlan.set_color_all_lights(default, rapid=True)

def get_pot_values(msg):
	print("msg = " + str(msg))
	print("len(msg) = " + str(len(msg)))
	noise_index = msg.find("N")
	color_index= msg.find("C")
	brightness_index = msg.find("B")
	kelvin_index = msg.find("K")

	noise_pot_value = msg[noise_index+1:]
	color_pot_value = msg[color_index+1:brightness_index]
	brightness_pot_value = msg[brightness_index+1:kelvin_index]
	kelvin_pot_value = msg[kelvin_index+1:noise_index]
	return noise_pot_value, color_pot_value, brightness_pot_value, kelvin_pot_value

def convert_raw_bulb_info(val, prev, tolerance, m, b, max_converted, bulb_on = True, min_converted = 0):
	# Mapping from raw pot values to color values

	# print("val = " + str(val))
	# print("prev = " + str(prev))

	if val == None:
		val = 0

	val = float(val)
	converted = m * val - b
	converted = int(converted)
	# print("initial converted = " + str(converted))

	# Eliminating extra potentiometer range
	if converted < 0:
		converted = 0
	if converted > max_converted:
		# print("setting to max")
		converted = max_converted

	if (converted < (prev + tolerance)) and (converted > (prev - tolerance)):
		# print("didn't depart from prev value enough")
		converted = prev
	else:
		# print("value has changed")
		prev = converted

	if not bulb_on:
		# print("setting converted to 0")
		converted = 0

	return converted, prev
