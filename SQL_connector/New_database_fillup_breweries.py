import mysql.connector
import pandas as pd

# Connect to MySQL
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="RobbeF",
    password="robbe",
    database="brewify"
)

# Create a cursor object to interact with the database
cursor = mydb.cursor()

# Read data from the text file
with open("BEB_unique_breweries_websites.txt", "r", encoding="utf-8") as file:
    next(file)  # Skip the header
    for line in file:
        print(line)

        try:
            # Split the line into the brewery_name and brewery_website
            brewery_name, brewery_website = line.strip().split("\t")
        except ValueError:
            print("Error: ", line)
            brewery_name = line.strip()
            brewery_website = "N/A"

        # Insert data into the breweries table
        insert_query = "INSERT INTO breweries (brewery_name, brewery_website) VALUES (%s, %s)"
        cursor.execute(insert_query, (brewery_name, brewery_website))

# Commit changes and close connection
mydb.commit()
mydb.close()
