import pandas as pd

beertable = pd.read_csv("../Datafiles/beernames.txt", sep="\t", index_col=False)

percentages = beertable["Percentage_Alcohol"]

fix = [str(percent).replace("%", "").replace(",", ".").replace("?", "NaN") for percent in percentages]
for i, perc in enumerate(fix):
    if perc == "":
        fix[i] = "NaN"

with open("../Datafiles/percentage.txt", "w") as f:
    for percent in fix:
        percent = str(percent)
        f.write(percent+"\n")
f.close()
