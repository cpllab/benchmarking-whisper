import whisper
from pyannote.audio import Pipeline
from pyannote_whisper.utils import diarize_text
import torch 
import pandas as pd
import os
import sys
import glob
import json
import time
import argparse
 = ""
print("Running CB1: yinruiqing")
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                    use_auth_token=YOURTOKEN)

# look for arguments to play around with 

parser = argparse.ArgumentParser()
parser.add_argument('audio_file_path', type=str)
parser.add_argument('specific_path', type=str) 
parser.add_argument('-beam_size', type=int, default = 5) 
parser.add_argument('-temperature', type=float, default = 0)    
parser.add_argument('-patience', type=float, default = None)    
parser.add_argument('-initial_prompt', type=str, default = None)   
parser.add_argument('-prompt', type=str, default = None)  
   
args = parser.parse_args()
    
audio_file_path = args.audio_file_path  
specific_path = args.specific_path
my_beam_size = args.beam_size 
my_temperature = args.temperature
my_patience = args.patience 
my_initial_prompt = args.initial_prompt 
my_prompt = args.prompt 


nameofdevice = "cuda" if torch.cuda.is_available() else "cpu"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(nameofdevice)

model = whisper.load_model("small.en") #Whisper model
model.to(device)
asr_result = model.transcribe(audio_file_path, beam_size = my_beam_size, temperature =my_temperature, patience=my_patience,language='english',initial_prompt = my_initial_prompt,prompt=my_prompt) #changing this

pipeline = pipeline.to(device)

diarization_result = pipeline(audio_file_path)
final_result = diarize_text(asr_result, diarization_result)

file_name = os.path.basename(audio_file_path)

speakerlist = []
textlist = []
starttimelist = []
endtimelist = []

for seg, spk, sent in final_result:
    line = f'{seg.start:.2f} {seg.end:.2f} {spk} {sent}'
    starttimelist.append(seg.start)
    endtimelist.append(seg.end)
    textlist.append(sent)
    speakerlist.append(spk)
    print(line)

dfdata = {
    'start_time': starttimelist,
    'end_time': endtimelist,
    'speaker': speakerlist,
    'text': textlist
}
df = pd.DataFrame(dfdata)


 
df.to_csv(specific_path, index=False)

 