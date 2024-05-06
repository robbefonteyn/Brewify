import pandas as pd

# load data from ratebeer_ratings_styles.txt
df = pd.read_csv("ratebeer_ratings_styles.txt", sep="\t")

# Create an empty dictionary to store profiles
profiles = {}

# Loop through each username
for username, group in df.groupby('username'):
    profile = {'preference': [], 'disliked': []}

    # Find preferred and disliked beer styles
    for index, row in group.iterrows():
        if row['taste_rating'] > 5:
            profile['preference'].append(row['beer_style'])
        elif row['taste_rating'] < 5:
            profile['disliked'].append(row['beer_style'])

    # Remove duplicate beer styles
    profile['preference'] = list(set(profile['preference']))
    profile['disliked'] = list(set(profile['disliked']))

    # Store the profile
    profiles[username] = profile


# Put the data into a dict and save it as a csv file
df = pd.DataFrame(profiles)
print(df)

# Print the profiles
for username, profile in profiles.items():
    print(f"Username: {username}")
    print(f"Preference: {profile['preference']}")
    print(f"Disliked: {profile['disliked']}")
    print()