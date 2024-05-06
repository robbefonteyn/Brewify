from urllib.request import urlopen
from bs4 import BeautifulSoup

# Initialize an empty list to store the beer information
beer_names = []
beer_IDs = []
breweries = []
beer_styles = []
abv = []
ibu = []
brewery_websites = []
location = []
out_of_production = []
length = 20177 # Number of beers on the website

for i in range(1, length):

    if i == 11029:
        continue

    if i > 11029:
        i -= 1

    print("Scraping beer number", i, "out of", length)

    url = "https://www.belgenbier.be/bieren/beschrijvingbier.php?idbieren=" + str(i)
    page = urlopen(url)
    html_bytes = page.read()
    try:
        html = html_bytes.decode("utf-8")

    except UnicodeDecodeError:
        html = html_bytes.decode("windows-1252")

    soup = BeautifulSoup(html, 'html.parser')

    # Get Beer Name
    beername_element = soup.find('div', id='col1')
    if beername_element is None:
        continue

    if "Etiketbier van:" in beername_element.getText():
        beer = beername_element.getText().strip()
        index = beer.find("  Etiketbier")
        beer = beer[:index].strip()
    else:
        beer = beername_element.getText().strip()

    if "(Uit productie) (No longer in production) (Ne plus en production)" in beer:
        out_of_production.append("No longer in production")
        index = beer.find("  (Uit productie)")
        beer = beer[:index].strip()
        print("Beer out of Production")
    else:
        out_of_production.append("N/A")

    print("Beer:", beer)
    beer_names.append(beer)

    # Get col2
    col2_element = soup.find('div', id="col2")

    # append beer ID
    beer_IDs.append(i)

    all_li = col2_element.find_all('li')
    # print("Number of li elements:", len(all_li))
    # print("all_li:", all_li)
    ibu.append("N/A")
    brewery_websites.append("N/A")

    for li in all_li:

        if "Info van de brouwer:" in li.getText():
            print(li.getText())
            continue

        if 'Brouwerij' in li.getText():
            test = li.getText()
            brewery_region = li.getText().rsplit(" - ", 1)
            brewery = brewery_region[0][33:].rstrip()
            print("Brewery:", brewery)
            breweries.append(brewery)
            print("Location:", brewery_region[1])
            location.append(brewery_region[1])

        if "Bierstijl" in li.getText():
            style = li.getText()[42:].rstrip()
            print("Style:", style)
            beer_styles.append(style)

        if 'Alcohol:' in li.getText():
            alcohol = li.getText()[9:].rstrip(" %")
            if alcohol == "Onbekend - Unknown - Inconnu":
                alcohol = "N/A"
            print("Alcohol:", alcohol)
            if alcohol != "N/A":
                abv.append(float(alcohol))
            else:
                abv.append(alcohol)

        if 'IBU' in li.getText():
            bitterness = li.getText()[38:].split(" => ")[0]
            print("IBU:", bitterness)
            if i > 11029:
                ibu[i - 2] = float(bitterness)
            else:
                ibu[i - 1] = float(bitterness)

        if 'Website' in li.getText():
            website = li.getText()[34:].rstrip()
            print("Website:", website)
            if i > 11029:
                brewery_websites[i - 2] = website
            else:
                brewery_websites[i - 1] = website

    percent = int((i / length) * 100)
    print("[", '#' * percent, str(percent) + "%", "." * (100 - percent), "]",
          "(" + str(i) + "/" + str(length) + ')')

info = {
    'Name': beer_names,
    'Brewery': breweries,
    'Style': beer_styles,
    'ABV': abv,
    'IBU': ibu,
    "Location": location,
    'Brewery Website': brewery_websites,
    "Out of Production": out_of_production
}

with open("abv_BEB.txt", "w", encoding="utf-8") as file:
    for a in abv:
        file.write(a + "\n")

with open("brewery_websites.txt", "w", encoding="utf-8") as file:
    for w in brewery_websites:
        file.write(w + "\n")

with open("ibu_BEB.txt", "w", encoding="utf-8") as file:
    for i in ibu:
        file.write(i + "\n")

with open("breweries_BEB.txt", "w", encoding="utf-8") as file:
    for b in breweries:
        file.write(b + "\n")
