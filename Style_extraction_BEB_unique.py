import pandas as pd
import numpy as np

# Read the dataset
data = pd.read_csv('BEB_fixed_beers.txt', encoding="utf-8", sep='\t')

# Extract unique styles
styles = data['Style'].tolist()

unique_style_list = []
#unique_style_list = {}
#
#for i in range(len(styles)):
#    if styles[i] not in unique_style_list:
#        unique_style_list[styles[i]] = 1
#    else:
#        unique_style_list[styles[i]] += 1
#

for i in range(len(styles)):
    if styles[i] not in unique_style_list:
        unique_style_list.append(styles[i])
    else:
        continue

print(unique_style_list)

unique_style = {
    "Styles": unique_style_list
}

df = pd.DataFrame(unique_style)
df.to_csv('BEB_unique_styles.txt', sep='\t', index=False)
