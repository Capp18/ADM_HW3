from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

columns = ["title", "intro", "plot", "film_name", "director", "producer", "writer", "starring", "music", "release_date", "runtime", "country", "language", "budget"]
a = np.empty((10000, 14,))
a[:] = np.nan
df = pd.DataFrame(data=a, columns=columns)

for i in range(9997):
    soup = BeautifulSoup(open("movies\\article_"+str(i)+".html", encoding="utf8"), "html.parser")
    #exctract the title
    df.iloc[i, 0] = soup.find("h1").text
    #extract the Intro
    Intro = ""
    par = soup.p # first paragraph of the html page
    while par.next_element.name != "h2" and par.next_element.name != "h3": # until a heading, combine all paragraphs
        if par.name == "p":
            Intro += par.get_text()
        par = par.next_element
    df.iloc[i, 1]=Intro

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
        df.iloc[i, 2] = Plot
    except AttributeError:
        continue

