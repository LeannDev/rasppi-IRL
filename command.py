import os
import subprocess
import time

from parameters import *

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

ffmpeg_command = (
    "ffmpeg -nostdin -f v4l2 {0} {1} -i {2} "
    "-f alsa -i {3} "
    "-i '{4}/image/location.svg' " 
    "-loop 1 -r .1 -i '{4}/image/social%d.svg' "
    "-filter_complex "
    '"{5}" '
    "-vcodec libx264 -rtbufsize 2000k {6} {7} -preset {8} -pix_fmt yuv420p -crf {9} -force_key_frames "
    "'expr:gte(t,n_forced*2)' -minrate 850k -maxrate 1000k -b:v 1000k -bufsize 1000k "
    "-acodec libmp3lame -rtbufsize 2000k -b:v 96k -ar 44100 -filter:a {10} -f flv 'rtmp://live.twitch.tv/app/{11}'"
    .format(
        "-s {0}".format(input_resolution) if input_resolution is not None else '',
        "-framerate {0}".format(input_framerate) if input_framerate is not None else '',
        input_video_device,
        input_audio_device,
        BASE_DIR,
        "overlay=x=20:y=17,overlay=x=20:y=H-h-20,drawtext=fontfile='{0}/fonts/UbuntuNerdFont.ttf':text='Buenos Aires, Argentina':fontcolor=white:fontsize=15:box=1:boxcolor=black@0.5:boxborderw=3:x=43:y=20,drawtext=fontfile='{0}/fonts/UbuntuNerdFont.ttf':textfile='{0}/socials/social1.txt':reload=1:fontcolor=white:fontsize=15:box=1:boxcolor=black@0.5:boxborderw=3:x=45:y=H-37" .format(BASE_DIR),
        "-s {0}".format(output_resolution) if output_resolution is not None else '',
        "-framerate {0}".format(output_framerate) if output_framerate is not None else '',
        preset,
        crf,
        volume,
        stream_key
    )
)

ping = subprocess.Popen(["ping", "-c 1", "8.8.8.8"], stdout=subprocess.PIPE)

ping.wait()

if ping.poll():
    print("Internet connection failed")
    time.sleep(60)

else:
    ffmpeg = subprocess.Popen(["bash","-c",ffmpeg_command], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    while True:
        ping = subprocess.Popen(["ping", "-c 1", "8.8.8.8"], stdout=subprocess.PIPE)
        ping.wait()

        if ping.poll():
            ffmpeg.terminate()
            print("Internet connection failed. Reconnecting...")

            ping = subprocess.Popen(["ping", "-c 1", "8.8.8.8"], stdout=subprocess.PIPE)
            ping.wait()

            while ping.poll() > 0:
               

                ping = subprocess.Popen(["ping", "-c 1", "8.8.8.8"], stdout=subprocess.PIPE)
                ping.wait()
                print("Reconnecting...")
                time.sleep(5)

            else:
                print("established connection")
                ffmpeg = subprocess.Popen(["bash","-c",ffmpeg_command], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        else:
            print("Stable connection")
            time.sleep(60)