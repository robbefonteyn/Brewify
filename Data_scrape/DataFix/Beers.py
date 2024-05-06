import pandas as pd

beertable = pd.read_csv("../Datafiles/beernames.txt", sep="\t", index_col=False)

beers = beertable["Merk"]

with open("../Datafiles/beers.txt", "w") as f:
    for beer in beers:
        beer = str(beer)
        f.write(beer+"\n")
f.close()
