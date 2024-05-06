beers = []
with open("../Datafiles/beers.txt", "r", encoding="utf-8") as b:
    for line in b.readlines():
        beers.append(line.rstrip())

styles = []
with open("../Datafiles/beertypes.txt", "r", encoding="utf-8") as t:
    for line in t.readlines():
        styles.append(line.rstrip())

percentages = []
with open("../Datafiles/percentage.txt", "r", encoding="utf-8") as p:
    for line in p.readlines():
        percentages.append(line.rstrip())

breweries = []
with open("../Datafiles/brewery.txt", "r", encoding="utf-8") as i:
    for line in i.readlines():
        breweries.append(line.rstrip())

startdates = []
with open("../Datafiles/startdate.txt", "r", encoding="utf-8") as d:
    for line in d.readlines():
        startdates.append(line.rstrip())

enddates = []
with open("../Datafiles/enddate.txt", "r", encoding="utf-8") as e:
    for line in e.readlines():
        enddates.append(line.rstrip())

ratings = []
with open("../Datafiles/beerratings.txt", "r", encoding="utf-8") as r:
    for line in r.readlines():
        ratings.append(line.rstrip())

data = {
    "beername": beers,
    "beer_style": styles,
    "alcohol_percentage": percentages,
    "brewery": breweries,
    "start_production": startdates,
    "end_production": enddates,
    "beer_rating": ratings
}

import pandas as pd

df = pd.DataFrame(data)
print(df)

df.to_csv("beernames.csv", sep="\t", index=False, encoding="utf-8")
