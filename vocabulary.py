import pandas as pd
"""
this script creates a vocabulary csv which contains the whole words contained
in the html files
"""
text =""
for film in range(10000):
    if film in [9429, 9671]: # the files with number 9429 and 9670 can not be downloaded because of an unexpected error because of that, they are excluded from the loop
        continue
    df = pd.read_csv("parsed_clean\\"+str(film)+".tsv", sep='\t', encoding='utf-8') #vocab read csv files
    df = df.fillna("")
    # get the intro and plot and combine them.
    intro = df.iloc[0, 1]
    plot = df.iloc[1, 1]
    text = text + " " + intro + " " + plot #concatanete all intros and plots for all films

arr = set(text.split()) # use set to eliminate repeating words
vocab = pd.DataFrame(arr)
vocab.to_csv("vocab.csv") #save vocabulary as csv with indices for each
