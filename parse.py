from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

columns = ["title", "intro", "plot", "film_name", "director", "producer", "writer", "starring", "music", "release_date","running time", "country", "language", "budget"]
a = np.empty((10000, 14,))
a[:] = np.nan
df = pd.DataFrame(data=a, columns=columns)

for film in range(10): # the index should be the number of the total files here 10 is just for quick trial :
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
    df.iloc[film, 1] = Intro

    # Parse the Plot
    for heading in soup.find_all(["h2", "h3"]):
        try:
            if (heading.contents[0].get("id") == "Plot" or heading.contents[0].get("id") == "Plot_summary" or
                heading.contents[0].get("id") == "Plot_Summary" or
                    heading.contents[0].get("id") == "Premise"): # first find the plot heading
                break
        except AttributeError:
            continue
    Plot = ""
    try:
        while heading.next_element.name != "h2" and heading.next_element.name != "h3": # starting from plot heading, concatanete all paragraphs
            if heading.name == "p":
                Plot += heading.get_text()
            heading = heading.next_element
        df.iloc[film, 2] = Plot
    except AttributeError:
        pass

    # Info box Parsing

    info_box = soup.find("table", {"class": "infobox vevent"})
    if info_box is None:
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

    df.iloc[film, :].to_csv("parsed\\"+str(film)+".tsv", sep='\t', encoding='utf-8') # create a different folder called parsed and save the tsv files in it


#df.iloc[0,:].to_excel("parsed\\parsing.xlsx")
