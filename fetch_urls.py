import time
import urllib.request
from bs4 import BeautifulSoup
from random import randint

"""
THIS SCRIPT IS FOR DOWNLOADING THE HTML FILES OF THE GIVEN DOCUMENTS
"""
soup = BeautifulSoup(open("movies1.html"), features="lxml") # create a soup object
url_list = []
for url in soup.findAll('a', href=True): # go through all links in the html file
    url_list.append(url['href']) # append urls ot a list
a = 9430, 9671
i = 0
while i <= (len(url_list)): # loop through all list and download the links as html files
    link = url_list[i]
    try:
        response = urllib.request.urlopen(link)
        webContent = response.read()
        with open("movies\\article_"+str(i)+".html", "wb")as file:
            file.write(webContent)
        time.sleep(randint(1, 5))
        print("in try ", i)
        i += 1
    except:
        print("in except ", i)
        time.sleep(120)

# the files with number 9429 and 9670 can not be downloaded because of an unexpected error






