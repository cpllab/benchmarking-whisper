import os
import pydub
from pydub import AudioSegment
 
chopping_dir = ""   
minute = 60 * 1000
n = 5


chopping_dir = '/om/user/arjunp/childes_test_random/'
for filename in os.listdir(chopping_dir):
    if filename.endswith(".mp3") or filename.endswith(".wav"):
        filepath = os.path.join(chopping_dir, filename)
        audio = AudioSegment.from_file(filepath)
        trimmed_audio = audio[ : n*minute]
        trimmed_audio.export(chopping_dir + filename[:-4] + "_first5.wav", format="wav")
 
