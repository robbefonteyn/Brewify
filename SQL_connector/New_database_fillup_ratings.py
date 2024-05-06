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

with open("Untappd_ratings.txt", "r", encoding="utf-8") as file:
    for rating in file:
        print(rating)

        rating = rating.strip()

        if pd.isna(rating) or rating == "nan":
            print("Error: ", rating)
            rating = None
        else:
            rating = float(rating)

        # Insert data into the ratings table
        insert_query = "INSERT INTO ratings (rating) VALUES (%s)"
        cursor.execute(insert_query, (rating,))

# Commit changes and close connection
mydb.commit()
mydb.close()
