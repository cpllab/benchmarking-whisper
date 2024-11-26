import subprocess
import os
for filename in os.listdir('/om/user/arjunp/childes_test_random'):
    if filename.endswith(".mp4"):
        filepath = os.path.join('/om/user/arjunp/childes_test_random', filename)    
        command = "ffmpeg -i " +filepath+ " -ab 160k -ac 2 -ar 44100 -vn "+ filename[:-4]+".wav"
        subprocess.call(command, shell=True)