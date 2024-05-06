from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

url = "http://localhost:63342/BrewMood/Data%20wrangeling/local_source.html?_ijt=4hrct9vtj3on2m2o540fmbrvle&_ij_reload=RELOAD_ON_SAVE"

page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")


db = []
merk = []
soort = []
percentage_alcohol = []
brouwerij = []
periode = []

soup = BeautifulSoup(html, 'html.parser')
td_texts = [td.get_text() for td in soup.find_all('td')]
current_beer = []

for linenr, text in enumerate(td_texts):
    if linenr >= 2:
        if text == '':
            text = "NaN"

        if linenr % 5 == 2:
            merk.append(text.rstrip().lstrip())
            current_beer.append(text.rstrip().lstrip())
        elif linenr % 5 == 3:
            soort.append(text.rstrip().lstrip())
            current_beer.append(text.rstrip().lstrip())
        elif linenr % 5 == 4:
            percentage_alcohol.append(text.rstrip().lstrip())
            current_beer.append(text.rstrip().lstrip())
        elif linenr % 5 == 0:
            brouwerij.append(text.rstrip().lstrip())
            current_beer.append(text.rstrip().lstrip())
        elif linenr % 5 == 1:
            periode.append(text.rstrip().lstrip())
            current_beer.append(text.rstrip().lstrip())

        if len(current_beer) == 5:
            db.append(current_beer)
            current_beer = []
data = {
    'Merk': merk,
    'Soort': soort,
    'Percentage Alcohol': percentage_alcohol,
    'Brouwerij': brouwerij,
    'Periode': periode
}

df = pd.DataFrame(data)
print(df)
