import pandas as pd
import subprocess
import glob
import json
import numpy as np
import time
from sklearn.metrics import mean_squared_error  
import math  
import pypandoc
import jiwer
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


## constants
codebasenameoptions = ['yinruiqing', 'speechbox', 'ashraf', 'whisperx']  
codebase_mapping_dict = {1: 'yinruiqing', 2: 'speechbox', 3: 'ashraf',4: 'whisperx'}
codebase_count_mapping_dict = {'count_cb1': 'yinruiqing', 'count_cb2': 'speechbox', 'count_cb3': 'ashraf', 'count_cb4': 'whisperx'}

## helper functions

def scrapeCBoutput(codebase_id, audiofilepath, unixtime):

    ''' 
    Function to scrape the csv output of a codebase and return the text output
    '''

    cb_alltext = []
    main_output_dir  = '/om/user/arjunp/pipelineOutput'
    audio_name = os.path.basename(audiofilepath)[:-4]

    codebasename = codebasenameoptions[codebase_id-1]

    csv_dir = os.path.join(main_output_dir, unixtime,codebasename)
    csv_path = os.path.join(csv_dir, audio_name+".csv")
    df = pd.read_csv(csv_path)
    cb_alltext.append(df['text'].astype(str).to_list())
     
    return cb_alltext


def parse_script(content):
    ''' 
    Function to scrape the srt script of a codebase
    '''

    lines = content.strip().split('\n')
    data = []
    for line in lines:
        match = re.match(r"(.+?): (.+)", line)
        if match:
            speaker = match.group(1).strip()
            dialogue = match.group(2).strip()
            data.append([speaker, dialogue])
    return data



def return_counts(corpus):
    ''' 
    Function to scrape token types and their frequencies from a corpus
    '''
    vectorizer = CountVectorizer(token_pattern=r'(?u)\b\w+\b')
    X = vectorizer.fit_transform(corpus)
    vocab = vectorizer.vocabulary_
    word_freq = X.toarray().sum(axis=0)
    word_freq_dict = {word: word_freq[idx] for word, idx in vocab.items()}
    return word_freq_dict


def createFullDataframe(name_of_audio, gold_transcript_path,unixtime): #evaluate for extensibility
    ''' 
    Function to create a dataframe comparing the gold standard transcript with the output of all codebases
    '''

    gold_standard_df = pd.read_csv(gold_transcript_path)
    gold_standard_counts = return_counts(gold_standard_df['text'])
    gold_df = pd.DataFrame(list(gold_standard_counts.items()) , columns=["token", "count"])
    all_scraped = []
    for i in range (1,5):
        all_scraped += scrapeCBoutput(i,name_of_audio,unixtime)   
     
    cb1_counts = return_counts(all_scraped[0])
    cb2_counts = return_counts(all_scraped[1])
    cb3_counts = return_counts(all_scraped[2])
    cb4_counts = return_counts(all_scraped[3])

    cb1_df = pd.DataFrame(list(cb1_counts.items()) , columns=["token", "count"])
    cb2_df = pd.DataFrame(list(cb2_counts.items()) , columns=["token", "count"])
    cb3_df = pd.DataFrame(list(cb3_counts.items()) , columns=["token", "count"])
    cb4_df = pd.DataFrame(list(cb4_counts.items()) , columns=["token", "count"])


    #loop this

    merge_step1 = pd.merge(gold_df, cb1_df, on='token', how='outer',suffixes=('_gold', '_cb1'))  
    merge_step2 = pd.merge(merge_step1, cb2_df, on='token', how='outer',suffixes=(None, '_cb2'))
    merge_step3 = pd.merge(merge_step2, cb3_df, on='token', how='outer',suffixes=(None, '_cb3'))
    merge_step4 = pd.merge(merge_step3, cb4_df, on='token', how='outer',suffixes=(None, '_cb4'))
    merge_step4.columns = ['token', 'count_gold', 'count_cb1', 'count_cb2','count_cb3', 'count_cb4']
    merge_step4.fillna(0, inplace=True)

    for i in range(1,5):
        merge_step4[f'count_cb{i}_residuals'] = merge_step4['count_gold'] - merge_step4[f'count_cb{i}']
        merge_step4[f'status_cb{i}'] = merge_step4[f'count_cb{i}_residuals'].apply(lambda x: 'undercount' if x > 0 else ('overcount' if x < 0 else 'exact'))
    merge_step4['audio'] = name_of_audio
    return merge_step4


def extractLatestTimestamp():
    subfolders = [int(f.name) for f in os.scandir('/om/user/arjunp/pipelineOutput') if f.is_dir()]
    return max(subfolders)


def prepareMyData(latest_timestamp=""):
    if latest_timestamp == "":
        latest_timestamp = str(extractLatestTimestamp())
    else:  
        time_directory = os.path.join('/om/user/arjunp/pipelineOutput',latest_timestamp)
    list_of_filepaths = glob.glob(os.path.join(time_directory, '**/*.csv'), recursive=True)
    list_of_files =  [os.path.basename(file)[:-4]  for file in list_of_filepaths] 
    list_of_audio =  [name+".wav" for name in list_of_files]
    list_of_gold_transcripts = []
    for name in list_of_files:
        if os.path.exists(os.path.join('/om/user/arjunp/goldTranscripts', name+"-IC.csv")):
            list_of_gold_transcripts.append(os.path.join('/om/user/arjunp/goldTranscripts', name+"-IC.csv"))
        else:
            list_of_gold_transcripts.append(os.path.join('/om/user/arjunp/goldTranscripts', name+".csv"))

    return   latest_timestamp, list_of_filepaths, list_of_files, list_of_audio, list_of_gold_transcripts