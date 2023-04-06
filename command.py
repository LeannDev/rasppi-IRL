import os
import subprocess
import time

from parameters import *

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

ffmpeg_command = (
    f"ffmpeg -nostdin -f v4l2 -vcodec mjpeg -s {input_resolution} -framerate {input_framerate} -i {input_video_device} "
    f"-f alsa -i {input_audio_device} "
    f"-i '{BASE_DIR}/image/location.svg' "
    # f"-filter_complex overlay=x=20:y=17,drawtext=fontfile='{BASE_DIR}/fonts/UbuntuNerdFont.ttf':text='Bariloche, Argentina':fontcolor=white:fontsize=15:box=1:boxcolor=black@0.5:boxborderw=3:x=43:y=20 "
    f"-vcodec libx264 -rtbufsize 2000k -s {output_resolution} -framerate {output_framerate} "
    f"-preset {preset} -pix_fmt yuv420p -crf {crf} -force_key_frames 'expr:gte(t,n_forced*2)' "
    "-minrate 850k -maxrate 1500k -b:v 1000k -bufsize 1000k -acodec libmp3lame -rtbufsize 2000k "
    "-b:v 96k -ar 44100 -f flv "
    f"rtmp://bue01.contribute.live-video.net/app/{stream_key}"
)

print(ffmpeg_command)

i = 0
status = False
seg = 60

def connection_status():
    # check ping
    ping = subprocess.Popen(["ping", "-c 1", "8.8.8.8"], stdout=subprocess.PIPE)
    ping.wait()

    if ping.poll():
        print("Internet connection failed")
        return False

    else:
        print("Stable connection")
        return True

def start_ffmpeg():
    # start ffmppeg subprocess command
    try:
        ffmpeg = subprocess.Popen(["bash","-c",ffmpeg_command], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(5)
        print('Start FFMPEG')
    except:
        ffmpeg = False
        print('Start FFMPEG ERROR')
    
    return ffmpeg

def ffmpeg_status(ffmpeg):
    poll = ffmpeg.poll()
    print('POLL ',poll)
    if poll is None:
        print('Subprocess is running')
        return True

    else:
        ffmpeg.kill()
        print('Killing subprocess')
        time.sleep(5)
        print('Subprocess kill')
        return False

ffmpeg = start_ffmpeg()
time.sleep(10)

while i < 300:

    if connection_status():
        if not ffmpeg_status(ffmpeg):
            ffmpeg = start_ffmpeg()
            print('FFMPEG ', ffmpeg)
            i = 0
            seg = 60
            time.sleep(10)

        else:
            seg = 60
            i = 0
        
    else:
        if ffmpeg:
            ffmpeg.kill()

        seg = 1
        i += 1

    time.sleep(seg)

