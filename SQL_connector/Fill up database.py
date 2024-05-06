import mysql.connector

# Connect to MySQL
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="RobbeF",
    password="robbe",
    database="brewify"
)

# Create a cursor object to interact with the database
cursor = mydb.cursor()

# Open the text file and read its contents
with open('BEB_fixed_beers.txt', 'r', encoding="utf-8") as file:
    entries = file.readlines()

# Iterate through each entry and insert into the database
for i, entry in enumerate(entries):

    # Skip the first line (header)
    if i == 0:
        continue

    # Assuming each entry is comma-separated
    entry_data = entry.strip().split("\t")

    name = entry_data[0]
    brewery = entry_data[1]
    style = entry_data[2]
    abv = entry_data[3]
    ibu = entry_data[4]
    location_name = entry_data[5]
    brewery_website = entry_data[6]
    try:
        out_of_production = entry_data[7]
    except:
        out_of_production = ""
        entry_data.append(out_of_production)
    #out_of_production = entry_data[7]

    # Insert data into MySQL table
    sql = (f'INSERT into temp_table_beers (beername, brewery, style, abv, ibu, location_name, brewery_website, '
           f'out_of_production) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)')
    cursor.execute(sql, entry_data)
    mydb.commit()  # Commit the transaction
    print(f"Inserted entry {i} into the database successfully.")


# Close cursor and MySQL connection
cursor.close()
mydb.close()
