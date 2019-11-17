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

