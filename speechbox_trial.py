import torch
from speechbox import ASRDiarizationPipeline
from datasets import load_dataset
import librosa
from datasets import Dataset
import numpy as np
import pandas as pd
import os
import sys 
import glob
import json
import time

device = "cuda:0" if torch.cuda.is_available() else "cpu"

pipeline1 = ASRDiarizationPipeline.from_pretrained("openai/whisper-small.en", device=device) #Whisper model choice

audio_file_path = sys.argv[1]
specific_path = sys.argv[2]

print("Running CB2: speechbox")
def data_loading():

    # Load the audio file

    file_name = os.path.basename(audio_file_path)
    y, sr = librosa.load(audio_file_path, sr=None)

    # Create a dictionary with your data
    data = {'audio': [y], 'sampling_rate': [sr]}

    # Create a Dataset object
    dataset = Dataset.from_dict(data)

    # Function to extract MFCC features
    def extract_mfcc(example):
        y = np.array(example['audio'])
        sr = example['sampling_rate']
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        return {'mfcc': mfcc.tolist()}

    # Apply the function to extract MFCC features
    dataset = dataset.map(extract_mfcc)

    # Convert the dataset to PyTorch tensors
    dataset = dataset.map(lambda example: {'mfcc': torch.tensor(example['mfcc'])})

    # Now you can use the dataset in your machine learning model
    return dataset[0],file_name



sample,file_name = data_loading()  
 
out = pipeline1(np.array (sample["audio"]))
print(out)

speakerlist = []
textlist = []
starttimelist = []
endtimelist = []
for d in out:
    starttimelist.append(d['timestamp'][0])
    endtimelist.append(d['timestamp'][1])
    textlist.append(d['text'])
    speakerlist.append(d['speaker'])

dfdata = {
    'start_time': starttimelist,
    'end_time': endtimelist,
    'speaker': speakerlist,
    'text': textlist
}
df = pd.DataFrame(dfdata)

 
df.to_csv(specific_path, index=False)
 