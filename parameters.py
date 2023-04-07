import os
from dotenv import load_dotenv

load_dotenv()

input_video_device = "/dev/video0"
input_audio_device = "hw:1,0"
input_resolution = "1280x720"
input_framerate = "30"
preset = "veryfast"
crf = "17"
output_resolution = "1280x720"
output_framerate = "30"
# volume = "loudnorm"

social_network = os.environ.get('SOCIAL')
location = "Buenos Aires, Argentina"
endpoint = "rtmp://bue01.contribute.live-video.net/app/" # Visit https://stream.twitch.tv/ingests/ for select your recommended endpoint
stream_key = api_key = os.environ.get('STREAMING_KEY')