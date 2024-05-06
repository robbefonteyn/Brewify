import pandas as pd
from deep_translator import GoogleTranslator

beertable = pd.read_csv("../Datafiles/beernames.txt", sep="\t")
print(beertable.shape)

# Change dates in the "Periode" collumn and divide into right types
# Also translate everything!
# Translated "Pils" wrong to "beer" -> Changed to "Pilsner"
beertypes = []
length = len(beertable["Soort"])

for number, beertype in enumerate(beertable["Soort"]):
    beertype = str(beertype)
    if beertype.lower() != "nan" or beertype != "?":
        translated = GoogleTranslator(source='dutch', target='en').translate(beertype)
        beertypes.append(translated)
        # print(beertype, "->", translated)
        percent = int((number / length) * 100)

        print("[", '#' * percent, str(percent) + "%", "." * (100 - percent), "]",
              "(" + str(number) + "/" + str(length) + ')')

    else:
        beertypes.append("NaN")
        print("NaN")

with open("../Datafiles/beertypes.txt", "w") as f:
    for beertype in beertypes:
        if beertype is None:
            beertype = "Nan"
        f.write(beertype + "\n")
f.close()
