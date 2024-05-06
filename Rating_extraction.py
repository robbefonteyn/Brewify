# Fix Untappd_ratings_ibu_production.txt and BEB_fixed_beers.txt
import pandas as pd

# Load the data
untap_df = pd.read_csv('Untappd_ratings_ibu_production.txt', sep='\t')
beb_df = pd.read_csv('BEB_fixed_beers.txt', sep='\t')

# Get lists
ibu_beb_list = beb_df['IBU'].tolist()
ibu_untap_list = untap_df['Untappd_ibu'].tolist()

prod_beb_list = beb_df['Out_of_Production'].tolist()
prod_untap_list = untap_df['production_status'].tolist()

# Fix the Untappd data
# Replacing IBU and Production Status in beb_df with the values from untap_df
for i in range(len(ibu_beb_list)):
    if pd.isna(ibu_beb_list[i]):
        ibu_beb_list[i] = ibu_untap_list[i]
    if pd.isna(prod_beb_list[i]):
        prod_beb_list[i] = prod_untap_list[i]

# Update the beb_df with the fixed data from the lists for column IBU and Out_of_Production
beb_df['IBU'] = ibu_beb_list
beb_df['Out_of_Production'] = prod_beb_list



# Save the fixed data
beb_df.to_csv('BEB_fixed_beers.txt', sep='\t', index=False)

print(beb_df)

# Extract ratings from Untappd_ratings_ibu_production.txt
# Load the data
untap_df = pd.read_csv('Untappd_ratings_ibu_production.txt', sep='\t')
ratings = untap_df['Untappd_rating'].tolist()

# Save the ratings
with open('Untappd_ratings.txt', 'w') as f:
    for rating in ratings:
        f.write(str(rating) + '\n')
