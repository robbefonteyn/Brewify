import pandas as pd

beertable = pd.read_csv("../Datafiles/beernames.txt", sep="\t", index_col=False)

period = beertable["Periode"]

startdate = []
enddate = []

for periode in period:
    periode = str(periode)
    if "-" in periode:
        split = periode.split("-")
        startdate.append(split[0])
        enddate.append(split[1])
    else:
        startdate.append("?")
        enddate.append("?")


with open("../Datafiles/startdate.txt", "w") as f:
    for date in startdate:
        f.write(date+"\n")
f.close()

with open("../Datafiles/enddate.txt", "w") as f:
    for date in enddate:
        f.write(date+"\n")
f.close()