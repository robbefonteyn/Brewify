import pandas as pd
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="RobbeF",
    password="robbe",
    database="brewify"
)


# Function to fetch data from the database
def fetch_data(query):
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

# Fetch all data from the users table
query = "SELECT * FROM users"
users_data = fetch_data(query)

# Dictionary to store preferred styles and disliked styles
preferred_styles = {}
disliked_styles = {}

# Function to process data and find preferred and disliked styles
def process_data(data):
    for row in data:
        user_id, _, preferred, disliked = row
        preferred_styles_list = preferred.split()
        disliked_styles_list = disliked.split()

        for style in preferred_styles_list:
            if style not in preferred_styles:
                preferred_styles[style] = set()
            preferred_styles[style].add(user_id)

        for style in disliked_styles_list:
            if style not in disliked_styles:
                disliked_styles[style] = set()
            disliked_styles[style].add(user_id)

# Process the users data
process_data(users_data)

# Function to find styles liked or disliked by users who like or dislike a particular style
def find_styles(styles_dict):
    result = {}
    for style, users in styles_dict.items():
        related_styles = {}
        for other_style, other_users in styles_dict.items():
            if style != other_style:
                common_users = users.intersection(other_users)
                if len(common_users) == len(users):
                    related_styles[other_style] = len(common_users)
        if related_styles:
            result[style] = related_styles
    return result

# Find preferred styles for each beerstyle
preferred_related_styles = find_styles(preferred_styles)

# Find disliked styles for each beerstyle
disliked_related_styles = find_styles(disliked_styles)

# Print results
print("Preferred Styles:")
for style, related_styles in preferred_related_styles.items():
    print(style + ":")
    for related_style, count in related_styles.items():
        print("   -", related_style, "(Liked by all", count, "users)")

print("\nDisliked Styles:")
for style, related_styles in disliked_related_styles.items():
    print(style + ":")
    for related_style, count in related_styles.items():
        print("   -", related_style, "(Disliked by all", count, "users)")

# Close the database connection
conn.close()
