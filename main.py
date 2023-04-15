import RPi.GPIO as GPIO
from time import time

from command import connection_status, start_ffmpeg, ffmpeg_status, check_process, kill_process

# set pines mode
GPIO.setmode(GPIO.BCM)

# Configure GPIO pin 3 as input with internal pull-up
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to be executed when the button is pressed
def button_callback(channel):

    # if there is internet connection, start ffmpeg
    if connection_status() and not check_process('ffmpeg'):
        ffmpeg = start_ffmpeg()

    else:
        kill_process('ffmpeg')

# Register callback function for event
GPIO.add_event_detect(3, GPIO.FALLING, callback=button_callback, bouncetime=300)

# Infinite loop to keep the script running
while True:
    pass
