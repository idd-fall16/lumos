import serial, string, os
import RPi.GPIO as GPIO
import time
# import multiprocessing

GPIO.setmode(GPIO.BCM)
# GPIO.setup(18, GPIO.OUT)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP))

while True:
    try:
        noise_state = GPIO.input(17)
        if noise_state == False:
            print("Button pressed")
            time.sleep(0.2)
        else:
            print("button off")
        # if (GPIO.input(17) == True):
        #     print("button pressed")
        # else:
        #     print("button off")
    except KeyboardInterrupt:
        exit()


# def audio_start(setting):
#   print('starting audio:' + str(setting))
#   volume = audio_map[setting][1]
#   audio = audio_map[setting][0]
#   os.system ('omxplayer -o local --vol ' + str(volume) + ' ' + audio)
#
# audio_map = {'1': ['jacobs_siri.mp3', -1200],
#         '2': ['relaxation.mp3', -1200],
#         '3': ['whitenoise.mp3', -1800],
#         '4': ['jacobs_serena.mp3', -1200]}
#
# def run_pillow(setting):
#   print('starting setting: ' + str(setting))
#   # motor_setting = motor_map[setting]
#   # motor_start(motor_setting)
#   audio_start(setting)
#   # aroma_start()
#
# def kill_threads():
#   print('killing threads')
#   global threads
#   for thread in threads:
#     thread.terminate()
#   threads = []
#
# output = ' '
# ser = serial.Serial('/dev/ttyACM0', 4800, timeout=1)
#
# while True:
#   while output != '':
#     output = ser.readline()
#     try:
#       run_pillow(output)
#     except KeyError:
#       pass
#   output = ' '
