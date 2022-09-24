from decouple import config 

input_video_device = "/dev/video0"
input_audio_device = "hw:1,0"
input_resolution = "1280x720"
input_framerate = "30"
preset = "ultrafast"
crf = "17"
output_resolution = "1280x720"
output_framerate = "30"
volume = "loudnorm"
stream_key = config('STREAM_KEY')