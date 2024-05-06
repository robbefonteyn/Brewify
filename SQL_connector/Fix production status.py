import pandas as pd
import mysql.connector

with open("untappd_ratings_ibu_production.txt", "r", encoding="utf-8") as file:
    next(file)
    production_status = []
    for line in file:
        beer_name, Untappd_rating, Untappd_ibu, stat = line.split("\t")
        production_status.append(stat.rstrip())


# Connect to MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="RobbeF",
        password="robbe",
        database="Brewify"
    )


# Function to update production status in beers table
def update_production_status(production_states):
    connection = connect_to_database()
    cursor = connection.cursor()
    beer_ids = [i for i in range(1395, 21562)]
    i = 0
    # Update production status for each state in the list
    for state in production_states:
        query = "UPDATE beers SET production_status = %s where beer_id = %s"
        cursor.execute(query, (state, beer_ids[i]))
        print(beer_ids[i], state)
        i += 1
        connection.commit()

    cursor.close()
    connection.close()


# Call the function to update production status
update_production_status(production_status)
