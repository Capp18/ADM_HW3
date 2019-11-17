import time
import urllib.request
from bs4 import BeautifulSoup
from random import randint
import pandas as pd

soup = BeautifulSoup(open(r"/Users/marcodicio/movies3.html"), features="lxml")
url_list = []
for url in soup.findAll('a', href=True):
    url_list.append(url['href'])
i =0 
while i <= (len(url_list)):
    link = url_list[i]
    try:
        response = urllib.request.urlopen(link)
        webContent = response.read()
        with open("/Users/marcodicio/Desktop/movies1/article_"+str(i)+".html", "wb")as file:
            file.write(webContent)
        time.sleep(randint(1, 5))
        print("in try ", i)
        i += 1
    except:
        print("in except ", i)
        time.sleep(100)

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string


columns = ["title", "intro", "plot", "film_name", "director", "producer", "writer", "starring", "music", "release_date","running time", "country", "language", "budget"]
a = np.empty((10000, 14,))
a[:] = np.nan
df = pd.DataFrame(data=a, columns=columns)

def clean_text(sentence):
    stop_words = set(stopwords.words("english"))
    tokens = RegexpTokenizer(r"\w+")
    porter = PorterStemmer()
    stem_words = list(map(porter.stem, tokens.tokenize(sentence)))
    words = filter(lambda x: x not in string.punctuation, stem_words)
    cleaned_text = filter(lambda x: x not in stop_words, words)
    return cleaned_text
    
for film in range(10000): # this is for the first file of movies
    if film in [1267,3664,5240,5873,7675,7721,7768,8053,8180,8273,8378,9229,9615]:
        continue
   
    
    soup = BeautifulSoup(open(r"/Users/marcodicio/Desktop/movies1/article_"+str(film)+".html", encoding="utf8"), "html.parser")
    #exctract the title
    df.iloc[film, 0] = soup.find("h1").text
    df.iloc[film, 3] = soup.find("h1").text
    #extract the Intro
    Intro = ""
    par = soup.p # first paragraph of the html page
    while par.next_element.name != "h2" and par.next_element.name != "h3": # until a heading, combine all paragraphs
        if par.name == "p":
            Intro += par.get_text()
        par = par.next_element
    # clean it with clean text function
    df.iloc[film, 1] = " ".join(list(clean_text(Intro)))

    # Parse the Plot
    for heading in soup.find_all(["h2", "h3"]):
        try:
            if (heading.contents[0].get("id") == "Plot" or heading.contents[0].get("id") == "Plot_summary" or
                heading.contents[0].get("id") == "Plot_Summary" or
                    heading.contents[0].get("id") == "Premise"): # first find the plot heading that can have different id's
                break
        except AttributeError:
            pass
    Plot = ""
    try:
        while heading.next_element.name != "h2" and heading.next_element.name != "h3": # starting from plot heading, concatanete all paragraphs
            if heading.name == "p":
                Plot += heading.get_text()
            heading = heading.next_element
        # clean it with clean text function
        df.iloc[film, 2] = " ".join(list(clean_text(Plot)))
    except AttributeError:
        pass

    # Info box Parsing

    info_box = soup.find("table", {"class": "infobox vevent"})
    if info_box is None:
        df.iloc[film, :].to_csv("/Users/marcodicio/Desktop/parsed_clean/" + str(film) + ".tsv", sep='\t', encoding='utf-8')
        continue
    tags = info_box.contents[0].contents # find tags in infobox
    for tr in tags:
        if len(tr.contents) == 2:
            flag = True
            s = tr.contents[0].get_text() # get the headings in infobox
            for i in range(len(columns)):
                sub_Str = s[:4].lower()
                target_str = columns[i]
                if sub_Str in target_str: # find correct column to write the relevant information
                    flag = False
                    break
            if flag:
                continue
            l = []
            if len(tr.contents[1].contents) > 1:
                for j in tr.contents[1].contents:
                    if j.string is not None:
                        l.append(j.string)
                df.iloc[film, i] = " ".join(l)
            else:
                df.iloc[film, i] = [tr.contents[1].get_text()]



    df.iloc[film, :].to_csv("/Users/marcodicio/Desktop/parsed_clean/"+str(film)+".tsv", sep='\t', encoding='utf-8')

import pandas as pd
"""
this script creates a vocabulary csv which contains the whole words contained
in the html files
"""
text =""
for film in range(10000):
    if film in [1267,3664,5240,5873,7675,7721,7768,8053,8180,8273,8378,9229,9615]: # the files with number 9429 and 9670 can not be downloaded because of an unexpected error because of that, they are excluded from the loop
        continue
    df = pd.read_csv("/Users/marcodicio/Desktop/parsed_clean/"+str(film)+".tsv", sep='\t', encoding='utf-8') #vocab read csv files
    df = df.fillna("")
    # get the intro and plot and combine them.
    intro = df.iloc[0, 1]
    plot = df.iloc[1, 1]
    text = text + " " + intro + " " + plot #concatanete all intros and plots for all films

arr = set(text.split()) # use set to eliminate repeating words
vocab = pd.DataFrame(arr)
vocab.to_csv("/Users/marcodicio/Desktop/vocab.csv") #save vocabulary as csv with indices for each
vocab




import pandas as pd
"""
This script creates inverted indices file for each word in vocabulary.csv

"""
vocab = pd.read_csv("/Users/marcodicio/Desktop/vocab.csv")
inverted_indices = {}
vocab = vocab.set_index("0").to_dict()["Unnamed: 0"] # set the keys of the inverted indices dictionary as the id's in vocabulary.csv
for index in range(len(vocab.values())):
    inverted_indices[index] = [] # set the values of inverted indices dictionary empty lists, later the documents containig relevant word
                                # would be appended to this list
for film in range(10000):
    text=""
    if film in [1267,3664,5240,5873,7675,7721,7768,8053,8180,8273,8378,9229,9615]:
        continue
    # get the intro + plot of each film as text
    df = pd.read_csv("/Users/marcodicio/Desktop/parsed_clean/"+str(film)+".tsv", sep='\t', encoding='utf-8')
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

idt = pd.read_csv("inverted_indices.csv").transpose() #op

idt.to_csv("/Users/marcodicio/Desktop/idt.csv")      
        



