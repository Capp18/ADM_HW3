from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import nltk
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

for film in range(10000): # the index should be the number of the total files here 10 is just for quick trial :
    if film in [9429, 9671]:
        continue
    soup = BeautifulSoup(open("movies\\article_"+str(film)+".html", encoding="utf8"), "html.parser")
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
                    heading.contents[0].get("id") == "Premise"): # first find the plot heading
                break
        except AttributeError:
            pass
    Plot = ""
    try:
        while heading.next_element.name != "h2" and heading.next_element.name != "h3": # starting from plot heading, concatanete all paragraphs
            if heading.name == "p":
                Plot += heading.get_text()
            heading = heading.next_element
        df.iloc[film, 2] = " ".join(list(clean_text(Plot)))
    except AttributeError:
        pass

    # Info box Parsing

    info_box = soup.find("table", {"class": "infobox vevent"})
    if info_box is None:
        df.iloc[film, :].to_csv("parsed_clean\\" + str(film) + ".tsv", sep='\t', encoding='utf-8')
        continue
    tags = info_box.contents[0].contents # find tags in infobox
    for tr in tags:
        if len(tr.contents) == 2:
            flag = True
            s = tr.contents[0].get_text() # get the headings in infobox
            for i in range(len(columns)):
                sub_Str = s[:4].lower()
                target_str = columns[i]
                if sub_Str in target_str: # find correct column to write the relevent information
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



    df.iloc[film, :].to_csv("parsed_clean\\"+str(film)+".tsv", sep='\t', encoding='utf-8') # create a different folder called parsed and save the tsv files in it


#df.iloc[0,:].to_excel("parsed\\parsing.xlsx")
