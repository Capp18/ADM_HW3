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
