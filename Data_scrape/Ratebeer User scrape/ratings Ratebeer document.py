import pandas as pd

# Load the beer data
beer_data = pd.read_csv(r'C:\Users\fonte\OneDrive - UGent\AJ 2023-2024\Biological '
                        r'Databases\Project\BrewMood\BEB_fixed_beers.txt', sep='\t')
beer_names = beer_data['Name'].tolist()
print(beer_names)

pathway = (r'C:\Users\fonte\OneDrive - UGent\AJ 2023-2024\Biological Databases\Project\BrewMood\Data_scrape\Ratebeer '
           r'User scrape\ratebeer.txt')

users = []
rated_beers = []
ratings = []
add = False
i = 0

# Look for users who have rated beers from beer_names list in the ratebeer.txt
with open(pathway, 'r') as f:
    for line in f.readlines():
        print(line)
        if "beer/name:" in line:
            pos_beer = line[12:]
            if pos_beer in beer_names:
                rated_beers.append(pos_beer)
                add = True
                print("Beer:", pos_beer)
            else:
                print("Not important beer")

        if "review/taste:" in line and add:
            rating = line[14:]
            ratings.append(rating)
            print("Rating:", rating)

        if "review/profileName:" in line and add:
            add = False
            username = line[20:]
            users.append(username)
            print("Username:", username)

print("Finished")
