import requests
from bs4 import BeautifulSoup
import pandas as pd


# Function to perform Google search and extract IBU
def get_IBU(beer_name):
    # Perform Google search
    search_query = f"{beer_name} untappd"
    search_url = f"https://www.google.com/search?q={search_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the first search result URL
        search_results = soup.find_all("a")
        first_result = None
        for result in search_results:
            href = result.get("href")
            if href and "untappd.com/b/" in href:
                first_result = href
                break

        # If no relevant result found
        if not first_result:
            print("No relevant results found.")
            return None

        # Fetch the IBU from the first result URL
        beer_page_response = requests.get(first_result, headers=headers)
        beer_page_response.raise_for_status()
        beer_soup = BeautifulSoup(beer_page_response.text, "html.parser")

        # Find and extract IBU
        ibu_tag = beer_soup.find("p", class_="ibu")
        if ibu_tag:
            ibu = ibu_tag.text.strip()
            return ibu
        else:
            print("IBU not found on the page.")
            return None

    except requests.exceptions.RequestException as e:
        print("Error occurred during request:", e)
        return None


# List of beer names
beer_data_path = r'C:\Users\Robbe Fonteyn\OneDrive - UGent\AJ 2023-2024\Biological Databases\Project\BrewMood\BEB_fixed_beers.txt'
beer_data = pd.read_csv(beer_data_path, sep='\t')
beer_names = beer_data['Name'].tolist()
brewery_names = beer_data['Brewery'].tolist()
ibus_list = []

# Get IBU for each beer
for beer in beer_names[:100]:
    print(f"Beer: {beer}")
    ibu = get_IBU(beer)
    if ibu != 'N/A IBU':
        print(f"IBU: {float(ibu.rstrip(' IBU'))}")
        ibus_list.append(float(ibu.rstrip(' IBU')))
    else:
        ibus_list.append('N/A')
        print("IBU not found.")
    print()
