import RPi.GPIO as GPIO
import time

from command import connection_status, start_ffmpeg, ffmpeg_status, check_process, kill_process

# set pines mode
GPIO.setmode(GPIO.BCM)

# Configure GPIO pin 3 as input with internal pull-up
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to be executed when the button is pressed
def button_callback(channel):
    time.sleep(0.05) # Wait 50ms to avoid button bounce

    # Check if there is an active network connection
    if connection_status():
        print('CONECTION OK')
        # Check if ffmpeg process is currently running
        process = check_process('ffmpeg')
        
        if process:
            print('IF PROCESS')
            # If ffmpeg process is currently running, kill it and wait for 10 seconds
            kill_process('ffmpeg')
            time.sleep(10)

        else:
            print('NOT PROCESS')
            # If ffmpeg process is not running and there is an active network connection, start the ffmpeg process and wait for 10 seconds
            ffmpeg = start_ffmpeg()
            time.sleep(10)

# Register callback function for event
GPIO.add_event_detect(3, GPIO.FALLING, callback=button_callback, bouncetime=1000)

# Infinite loop to keep the script running
while True:
    time.sleep(1)
