import requests
from bs4 import BeautifulSoup

with open("beers.txt", "r", encoding="utf-8") as f:
    # Using list comprehension for conciseness
    beer_names = [line.rstrip('\n') for line in f]
    print(beer_names)
f.close()

beer_ratings = []
length = len(beer_names)

for number, beer_name in enumerate(beer_names):
    # Build a search URL (modify as needed)
    url = f'https://untappd.com/search?q="{beer_name}"'

    # Make a request (add headers and delays for responsible scraping)
    response = requests.get(url, headers={"User-Agent": "BrewMood Rating scraper"})
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract rating information (modify based on Untappd's HTML structure)
    rating_element = soup.find("span", class_="num")

    if rating_element:
        rating = rating_element.text
        rating = rating.lstrip("(").rstrip(")")
    else:
        rating = "No Rating Found"

    beer_ratings.append(rating)
    percent = int((number / length) * 100)

    print("[", '#' * percent, str(percent) + "%", "." * (100 - percent), "]",
          "(" + str(number) + "/" + str(length) + ')')


print("Done")

with open("beerratings.txt", "w") as f:
    for rating in beer_ratings:
        if rating == "0":
            rating = "No Rating Found"
        f.write(rating + "\n")
f.close()
