import requests
from bs4 import BeautifulSoup
import pandas as pd

beer_data_path = r'C:\Users\Robbe Fonteyn\OneDrive - UGent\AJ 2023-2024\Biological Databases\Project\BrewMood\BEB_fixed_beers.txt'
beer_data = pd.read_csv(beer_data_path, sep='\t')
beer_names = beer_data['Name'].tolist()
brewery_names = beer_data['Brewery'].tolist()
ibus_list = []
beer_ratings = []
production_status = []

length = len(beer_names)

for beer_name in beer_names:
    # Build a search URL (modify as needed)
    url = f'https://untappd.com/search?q="{beer_name}"'

    # Make a request (add headers and delays for responsible scraping)
    response = requests.get(url, headers={"User-Agent": "BrewMood Rating scraper"})
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract rating information (modify based on Untappd's HTML structure)
    no_results = soup.find("div", class_="results-none")

    rating_element = soup.find("span", class_="num")

    ibu_tag = soup.find("p", class_="ibu")

    production_tag = soup.find("p", class_="oop")
    print(production_tag)

    if not no_results:
        if ibu_tag:
            ibu = ibu_tag.text.strip()
            if ibu != "N/A IBU":
                ibus_list.append(float(ibu.rstrip(' IBU')))
            else:
                ibus_list.append('N/A')

        if rating_element:
            rating = rating_element.text
            rating = rating.lstrip("(").rstrip(")")
        else:
            rating = "N/A"

        if rating == "0":
            rating = "N/A"

        beer_ratings.append(rating)

        if production_tag:
            production_status.append(production_tag.text.strip())
        else:
            if rating == "N/A":
                production_status.append("N/A")
            else:
                production_status.append("Available")

    else:
        print("No results found for this beer.")
        ibus_list.append("N/A")
        beer_ratings.append("N/A")
        production_status.append("N/A")

    print(f"Beer: {beer_name}")
    print(f"Rating: {beer_ratings[-1]}")
    print(f"IBU: {ibus_list[-1]}")
    print(f"Production status: {production_status[-1]}")
    print()
