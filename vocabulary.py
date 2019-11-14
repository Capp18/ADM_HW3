import pandas as pd
text =""
for film in range(10000): # the index should be the number of the total files here 10 is just for quick trial :
    if film in [9429, 9671]:
        continue
    df = pd.read_csv("parsed_clean\\"+str(film)+".tsv", sep='\t', encoding='utf-8')
    df = df.fillna("")
    intro = df.iloc[0, 1]
    plot = df.iloc[1, 1]
    text = text + " " + intro + " " + plot

arr = set(text.split())
vocab = pd.DataFrame(arr)
vocab.to_csv("vocab.csv")