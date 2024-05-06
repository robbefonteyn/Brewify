import re
import pandas as pd

# Load the beer data
beer_data_path = r'C:\Users\Robbe Fonteyn\OneDrive - UGent\AJ 2023-2024\Biological Databases\Project\BrewMood\BEB_fixed_beers.txt'
beer_data = pd.read_csv(beer_data_path, sep='\t')
beer_names = beer_data['Name'].tolist()

pathway = r'C:\Users\Robbe Fonteyn\OneDrive - UGent\AJ 2023-2024\Biological Databases\Project\BrewMood\Data_scrape\Ratebeer User scrape\ratebeer.txt'

# Lists to store profile names and taste ratings
profile_names = []
taste_ratings = []
rated_beers = []

# Reading the text file
with open(pathway, "r") as file:
    data = file.read()
    print("Data finished reading")

# Regular expression to extract beer names, profile names, and taste ratings
pattern = re.compile(r'beer/name: (.*?)\n.*?review/profileName: (.*?)\n.*?review/taste: (\d+)/10', re.S)

# Finding all matches
matches = re.findall(pattern, data)

# Iterating through matches
for match in matches:
    beer_name, profile_name, taste_rating = match
    # Check if the beer name is in the beer_names list
    if beer_name in beer_names:
        profile_names.append(profile_name)
        taste_ratings.append(int(taste_rating))
        rated_beers.append(beer_name)
        print(beer_name, profile_name, taste_rating)

# Printing or using the lists
print("Profile Names:", profile_names)
print("Taste Ratings:", taste_ratings)
