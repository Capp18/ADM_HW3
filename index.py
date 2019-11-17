this script creates a vocabulary csv which contains the whole words contained
in the html files
"""
import pandas as pd
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

"""
This script creates inverted indices file for each word in vocabulary.csv

"""
vocab = pd.read_csv("vocab.csv")
inverted_indices = {}
vocab = vocab.set_index("0").to_dict()["Unnamed: 0"] # set the keys of the inverted indices dictionary as the id's in vocabulary.csv
for index in range(len(vocab.values())):
    inverted_indices[index] = [] # set the values of inverted indices dictionary empty lists, later the documents containig relevant word
                                # would be appended to this list
for film in range(10000):
    text=""
    if film in [9429, 9671]:
        continue
    # get the intro + plot of each film as text
    df = pd.read_csv("parsed_clean\\"+str(film)+".tsv", sep='\t', encoding='utf-8')
    df = df.fillna("")
    intro = df.iloc[0, 1]
    plot = df.iloc[1, 1]
    text = intro + " " + plot
    # go through each word in the text and ad the document to the value in the inverted indicies dictionary
    for word in text.split():
        try:
            term_id =int(vocab[word.lower()])
            inverted_indices[term_id].append("doc_"+str(film))
        except KeyError:
            continue
# save the dictionary as csv
import csv
with open('inverted_indices.csv', "w") as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, inverted_indices.keys())
    w.writeheader()
    w.writerow(inverted_indices)

op=pd.read_csv("inverted_indices.csv").transpose()
#########################################################################################
from sklearn.feature_extraction.text import TfidfVectorizer

vocabulary=[]
for i in vocab.index:
    vocabulary.append(vocab[0][i])  #A list of all words in all documents


inverted_indices = {}  #Initialization of the vocabulary: for each word there is a list of documents in which it is contained in and the relative tfIdf score

for el in vocabulary:
    inverted_indices[el] = []
for film in range(9999):
    text=""
    if film in [5520,5576,7725,8100]:
        continue
    df = pd.read_csv("C:/Users/Capp/Documents/Università/Magistrale/1-ADM/Homework3/parsed_clean\\"+str(film)+".tsv", sep='\t', encoding='utf-8')
    df = df.fillna("")
    intro = df.iloc[0, 1]
    plot = df.iloc[1, 1]
    text = intro + " " + plot
    
    voc=text.split()   #List of words contained in the document
    vectorizer=TfidfVectorizer()
    vec=vectorizer.fit_transform(voc) #Matrix of the tfIdf score for every word contained in the document
    
    for i in range(len(voc)):
        try:
            if (["doc_"+str(film),''.join((str(vec[i])[3:-5]).split())]) not in inverted_indices[voc[i]]:
                inverted_indices[voc[i]].append(["doc_"+str(film),''.join((str(vec[i])[3:-5]).split())])
            else:
                pass
        except KeyError:
            continue
import json
with open('C:/Users/Capp/Documents/Università/Magistrale/1-ADM/Homework3/inverted_indices.json', "w") as f:  # Just use 'w' mode in 3.x
    json.dump(inverted_indices, f)
