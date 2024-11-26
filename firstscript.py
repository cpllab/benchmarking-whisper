print("Hello, Openmind!")
#import librosa
print("librosa imported")
import torch
print("torch imported")
from pyannote.audio import Pipeline
print("pyannote imported")
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",use_auth_token="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")
print("pipeline set up!")