import mysql.connector
import pandas as pd

# Connect to MySQL
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="RobbeF",
    password="robbe",
    database="brewify"
)

# Initialize an empty dictionary to store the data
styles_dict = {}

# Read data from the file
with open("styles_id.txt", "r") as file:
    for line in file:
        style_id, beer_style = line.strip().split("\t")
        # Convert style_id to integer
        style_id = int(style_id)
        # Add data to the dictionary
        styles_dict[beer_style] = style_id

# Initialize an empty dictionary to store the brewery ids
breweries_dict = {}

# Read data from the file
with open("breweries_id.txt", "r") as file:
    for line in file:
        brewery_id, brewery_name = line.strip().split("\t")
        # Convert brewery_id to integer
        brewery_id = int(brewery_id)
        # Add data to the dictionary
        breweries_dict[brewery_name] = brewery_id


# Fill up beers table, columns are: beer_id, beer_name, brewery_id, style_id, ibu, abv, location_name, rating_id,
# production_status
cursor = mydb.cursor()
rating_range = list(range(55, 20222))

with open("BEB_fixed_beers.txt", "r", encoding="utf-8") as file:
    rating_id = 54
    next(file)  # Skip the header
    for line in file:
        line = line.strip()
        beer_name, brewery, style, abv, ibu, location_name, brewery_website, production_status = line.split("\t")

        # Increase rating_id
        rating_id += 1

        # Check if the brewery is in the breweries_dict
        if brewery in breweries_dict:
            brewery_id = breweries_dict[brewery]
        else:
            brewery_id = None

        # Check if the style is in the styles_dict
        if style in styles_dict:
            style_id = styles_dict[style]
        else:
            style_id = None

        # Check if any of the variables is equal to "N/A" or "nan"
        if pd.isna(abv) or abv == "nan" or abv == "N/A":
            abv = None
        else:
            abv = float(abv)

        if pd.isna(ibu) or ibu == "nan" or ibu == "N/A":
            ibu = None
        else:
            ibu = float(ibu)

        if pd.isna(production_status) or production_status == "nan" or production_status == "N/A":
            production_status = None

        if pd.isna(location_name) or location_name == "nan" or location_name == "N/A":
            location_name = None

        print("beer_name: ", beer_name)
        print("brewery_id: ", brewery_id)
        print("style_id: ", style_id)
        print("ibu: ", ibu)
        print("abv: ", abv)
        print("location_name: ", location_name)
        print("rating_id: ", rating_id)
        print("production_status: ", production_status)
        print()

        # Insert data into the beers table
        insert_query = "INSERT INTO beers (beer_name, brewery_id, style_id, ibu, abv, location_name, rating_id, production_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (beer_name, brewery_id, style_id, ibu, abv, location_name, rating_id, production_status))

# Commit changes
mydb.commit()
mydb.close()


