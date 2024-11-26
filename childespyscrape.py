import pandas as pd
import childespy as chp 
import os 

 
corpus_list = ['Rollins','TD']

for nameofcorpus in corpus_list:
    try:
        df = chp.get_utterances(corpus = nameofcorpus)
        filepath = os.path.join('/om/user/arjunp/allChildesScrape', nameofcorpus+".csv")
        df.to_csv(filepath, index=False)
    except:
        print(nameofcorpus)
        continue