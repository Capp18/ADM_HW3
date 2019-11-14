import pandas as pd
vocab = pd.read_csv("vocab.csv")
vocab = vocab.set_index("0").to_dict()["Unnamed: 0"]
op = pd.read_csv("inverted_indices.csv").transpose()

sentence = "submarin"

htmls = []
for word in sentence.split():
    try:
        id = vocab[word]
    except KeyError:
        continue
    doc = op.iloc[id]
    htmls.append(doc)
