"""
This script is the first search engine without a score
returns title, intro and url for relevant films
"""
import pandas as pd
from bs4 import BeautifulSoup
import re
# get the urls of each movie
soup = BeautifulSoup(open("movies1.html"), features="lxml")
url_list = []
for url in soup.findAll('a', href=True):
    url_list.append(url['href'])

# import the vocab csv
vocab = pd.read_csv("vocab.csv")
vocab = vocab.set_index("0").to_dict()["Unnamed: 0"]
op = pd.read_csv("inverted_indices.csv").transpose()

sentence = "lion king"

htmls = []
for word in sentence.split(): # go trough each word in sentence and match the word with id's in vocab csv
    try:
        id = vocab[word]
    except KeyError:
        word = word[:-1] # sometimes the last letter of a word is droped when nltk library used because of an un known reason
        try:            # to overcome this, the matching is done with eliminating the last letter
            id = vocab[word]
        except KeyError:
            continue

    doc = op.iloc[id].values[0].split()
    doc[0] = doc[0][1:]
    doc[-1] = doc[-1][:-1]
    htmls.append(set(doc))

# use set intersection to get the documents containing all words
intersection = set.intersection(*htmls)
# create a results dataframe to store the info
results = pd.DataFrame({'Title': [], 'Intro': [], 'url': []})
counter = 0
for document in intersection:
    document = re.findall(r'\d+', document)[0]

    soup = BeautifulSoup(open("movies\\article_" + document + ".html", encoding="utf8"), "html.parser")
    # get title ( same in parse)
    title = soup.find("h1").text
    # get intro (same in parse)
    Intro = ""
    par = soup.p # first paragraph of the html page
    while par.next_element.name != "h2" and par.next_element.name != "h3": # until a heading, combine all paragraphs
        if par.name == "p":
            Intro += par.get_text()
        par = par.next_element
    # get url ( same in fetch_urls)
    url = url_list[int(document)]
    results.loc[counter] = [title, Intro, url]
    counter += 1

print(results)
############################################################################################################
#SEARCH ENGINE 2 (NOT COMPLETED)
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import json
from sklearn.feature_extraction.text import TfidfVectorizer

with open('C:/Users/Capp/Documents/Università/Magistrale/1-ADM/Homework3/inverted_indices_score.json', "r") as f:  # Just use 'w' mode in 3.x
    inverted_indices=json.load(f)
sentence=input()
def clean_text(sentence):
    stop_words = set(stopwords.words("english"))
    tokens = RegexpTokenizer(r"\w+")
    porter = PorterStemmer()
    stem_words = list(map(porter.stem, tokens.tokenize(sentence)))
    words = filter(lambda x: x not in string.punctuation, stem_words)
    cleaned_text = filter(lambda x: x not in stop_words, words)
    return string

query={}
vectorizer=TfidfVectorizer()
v=vectorizer.fit_transform(string)
for i in range(len(string)):
    query[string[i]]=''.join((str(v[i])[3:-5]).split())
##
l=[]
for el in string:
    se=set()
    for i in range(len(inverted_indices[el])):
        se=se|{inverted_indices[el][i][0]}
    l.append(se)
docs=l[0]
for i in range(1,len(l)):
    docs=docs&l[i-1]

n={}
d1={}
d2={}
for doc in docs:
    for el in string:
        query[el]='0.'+query[el][2:len(query[el])]
        y=float(query[el])
        for i in range(len((inverted_indices[el]))):
            if inverted_indices[el][i][0]==doc:
                inv='0.'+inverted_indices[el][i][1][2:len(inverted_indices[el][i][1])]
                x=float(inv)
                if inverted_indices[el][i][0] not in n:
                    n[inverted_indices[el][i][0]]=(x*y)
                else:
                    n[inverted_indices[el][i][0]]+=(x*y) #Summation of numerator
                ##
                if inverted_indices[el][i][0] not in d1:
                    d1[inverted_indices[el][i][0]]=x**2
                else:
                    d1[inverted_indices[el][i][0]]+=x**2 #summation of first part denominator
                ##
                if inverted_indices[el][i][0] not in d2:
                    d2[inverted_indices[el][i][0]]=y**2
                else:
                    d2[inverted_indices[el][i][0]]+=y**2 #summation of second part denominator
            else:
                pass
results={}  #A dictionary with all documents and relatives cosine similarity values
for el in n:
    try:
        results[el]=(n[el])/((d1[el])**(1/2))*((d2[el])**(1/2))
    except ZeroDivisionError:
        continue
