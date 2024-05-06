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

with open("BEB_unique_styles.txt", "r", encoding="utf-8") as file:
    next(file)  # Skip the header
    for line in file:
        print(line)

        try:
            # Split the line into the style_name
            style_name = line.strip()
        except ValueError:
            print("Error: ", line)
            style_name = line.strip()

        # Insert data into the styles table
        insert_query = "INSERT INTO styles (style_name) VALUES (%s)"
        cursor.execute(insert_query, (style_name,))

# Commit changes and close connection
mydb.commit()
mydb.close()
