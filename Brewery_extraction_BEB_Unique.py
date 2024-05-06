import pandas as pd
import numpy as np

# Read the dataset
data = pd.read_csv('BEB_fixed_beers.txt', encoding="utf-8", sep='\t')

# Extract unique breweries and unique brewery websites
breweries = data['Brewery'].tolist()
websites = data['Brewery_Website'].tolist()

unique_brew_list = []
unique_web_list = []

for i in range(len(breweries)):
    if breweries[i] not in unique_brew_list:
        unique_brew_list.append(breweries[i])
        if websites[i] is None or websites[i] == 'N/A' or websites[i] == 'nan' or websites[i] == np.nan:
            unique_web_list.append('N/A')
        else:
            unique_web_list.append(websites[i])

# To a dict
unique_brewery_info = {
    "Breweries": unique_brew_list,
    "Websites": unique_web_list
}

# To a dataframe
df = pd.DataFrame(unique_brewery_info)

# Save the unique breweries and websites to a file
df.to_csv('BEB_unique_breweries_websites.txt', sep='\t', index=False)
