import pandas as pd

beertable = pd.read_csv("../Datafiles/beernames.txt", sep="\t", index_col=False)

brewery = beertable["Brouwerij"]

with open("../Datafiles/BEB_breweries.txt", "w") as f:

    for brew in brewery:
        brew = str(brew)
        f.write(brew+"\n")
f.close()
