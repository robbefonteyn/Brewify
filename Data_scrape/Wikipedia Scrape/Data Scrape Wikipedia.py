import pandas as pd

beers_table = pd.read_html("https://nl.wikipedia.org/wiki/Lijst_van_Belgische_bieren")
all_beers = []
for i, table in enumerate(beers_table):
    all_beers.append(table)
belgian_beers_df = pd.concat(all_beers, ignore_index=True)

belgian_beers_df.to_csv("output.txt", sep="\t", index=False)
print(belgian_beers_df)