import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="RobbeF",
    password="robbe",
    database="brewify"
)

cursor = mydb.cursor(buffered=True)
beers_to_add = []
beer_styles = []

with open("ratebeer_ratings.txt", "r", encoding="utf-8") as file:
    entries = file.readlines()
    for entry in entries:
        beername, username, taste_rating = entry.strip().split("\t")
        beers_to_add.append(beername)

for beer in beers_to_add:
    print("Beer: ", beer)
    sql = f"SELECT s.style_name FROM beers b INNER JOIN styles s ON b.style_id = s.style_id WHERE b.beer_name = %s"

    cursor.execute(sql, (beer,))
    style = cursor.fetchone()

    if style:
        beer_styles.append(style[0])
        print("Style:",style[0])
        print()
    else:
        beer_styles.append("None")

cursor.close()
mydb.close()

print(beer_styles)
