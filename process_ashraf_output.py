import pandas as pd
import os
import sys
import glob
import json
import time
srtfilepath = sys.argv[1]
specific_path = sys.argv[2]

def parse_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        file_name = os.path.basename(file_path)

    subtitles = []
    for block in content.strip().split('\n\n'):
        lines = block.split('\n')
        #index = int(lines[0])
        timecodes = lines[1].split(' --> ')
        start = timecodes[0]
        end = timecodes[1]
        text = '\n'.join(lines[2:])
        subtitles.append({
             
            'start': start,
            'end': end,
            'text': text
        })

    return subtitles,file_name

# Example usage
subtitles,file_name = parse_srt(srtfilepath)


speakerlist = []
textlist = []
starttimelist = []
endtimelist = []
for sub in subtitles:
    starttimelist.append(sub['start'])
    endtimelist.append(sub['end'])
    speakerplustext = sub['text']
    char_of_colon = speakerplustext.find(':')
    textlist.append(speakerplustext[char_of_colon+2:])
    speakerlist.append(speakerplustext[:char_of_colon])

dfdata = {
    'start_time': starttimelist,
    'end_time': endtimelist,
    'speaker': speakerlist,
    'text': textlist
}
df = pd.DataFrame(dfdata)

 
df.to_csv(specific_path, index=False)
 