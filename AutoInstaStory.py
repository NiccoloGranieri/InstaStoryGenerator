from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioClip, AudioFileClip, concatenate_audioclips
import moviepy.audio.fx.audio_fadein, moviepy.audio.fx.audio_fadeout

import uuid
import random

import os
import sys

# Creation of a random string for temp filenames
def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length] # Return the random string.
videoToCrop = []
deleteTmp = False

try:
    video = sys.argv[1]
    clipLength = VideoFileClip(video)
    length = clipLength.duration
except IndexError:
    print("Please provide a file name to parse.")
    sys.exit()

if len(sys.argv) >= 3:
    deleteTmp = True
    for x in range (1, len(sys.argv)):
        video = sys.argv[x]
        videoToCrop.append(VideoFileClip(video))
#   combinVid = concatenate_videoclips([videoToCrop[0], videoToCrop[1]])
    combinVid = concatenate_videoclips(videoToCrop)
    rndStr = my_random_string(10)
    print rndStr
    tempName = "temp_" + rndStr + ".mp4"
    combinVid.write_videofile(tempName, 
        codec='libx264', 
        audio_codec='aac', 
        temp_audiofile='temp-audio.m4a', 
        remove_temp=True
    )
    video = (tempName)
    clipLength = VideoFileClip(video)
    length = clipLength.duration
else:
    video = sys.argv[1]

clipArr = []
soundArr = []
sFXArr = []
randArr = []

oneFifteenth = int(length) / 15
endSec = oneFifteenth
startSec = 1

notification = False

for x in range(15):
    if notification is False:
        print "[MoviePy] Cutting audio and video up..."
        notification = True
    randArr.append(random.randint(startSec, endSec))
    clipArr.append(VideoFileClip(video).subclip(randArr[x], randArr[x] + 1))
    soundArr.append(AudioFileClip(video).subclip(randArr[x], randArr[x] + 1))
    sFXArr.append((soundArr[x].audio_fadein(0.01)
                              .audio_fadeout(0.01)))
    startSec = endSec 
    endSec += oneFifteenth

# Combine Video Clips
# final_clip = concatenate_videoclips([clipArr[0], clipArr[1], clipArr[2], clipArr[3], clipArr[4], clipArr[5], clipArr[6], clipArr[7], clipArr[8], clipArr[9], clipArr[10], clipArr[11], clipArr[12], clipArr[13], clipArr[14]])
final_clip = concatenate_videoclips(clipArr)

final_clip_rot = final_clip.rotate(90)

# Combine Audio Clips
# final_audio = concatenate_audioclips([sFXArr[0], sFXArr[1], sFXArr[2], sFXArr[3], sFXArr[4], sFXArr[5], sFXArr[6], sFXArr[7], sFXArr[8], sFXArr[9], sFXArr[10], sFXArr[11], sFXArr[12], sFXArr[13], sFXArr[14]])
final_audio = concatenate_audioclips(sFXArr)

# Stitch Audio and Video Together
combClip = final_clip_rot.set_audio(final_audio)

# Write Video File to Disk
combClip.write_videofile("my_concatenation.mp4", 
  codec='libx264',
  audio_codec='aac', 
  temp_audiofile='temp-audio.m4a', 
  remove_temp=True
)

if deleteTmp == True:
    os.remove(tempName)