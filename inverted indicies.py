import pandas as pd
vocab = pd.read_csv("vocab.csv")
inverted_indices = {}
vocab = vocab.set_index("0").to_dict()["Unnamed: 0"]
for index in range(len(vocab.values())):
    inverted_indices[index] = []
for film in range(10000):
    text=""
    if film in [9429, 9671]:
        continue
    df = pd.read_csv("parsed_clean\\"+str(film)+".tsv", sep='\t', encoding='utf-8')
    df = df.fillna("")
    intro = df.iloc[0, 1]
    plot = df.iloc[1, 1]
    text = intro + " " + plot
    for word in text.split():
        try:
            inverted_indices[int(vocab[word.lower()])].append("doc_"+str(film))
        except KeyError:
            continue
import csv
with open('inverted_indices.csv', "w") as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, inverted_indices.keys())
    w.writeheader()
    w.writerow(inverted_indices)
    
op=pd.read_csv("inverted_indices.csv").transpose()