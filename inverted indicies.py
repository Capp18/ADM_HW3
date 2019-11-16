import pandas as pd
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