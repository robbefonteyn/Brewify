import mysql.connector
import pandas as pd

#Load data
df = pd.read_csv("Userprofiles.txt", sep="\t")

# Convert the list of prefered and disliked beerstyles to a string
df['preference'] = df['preference'].apply(lambda x: x.replace('[','').replace(']','').replace('\'','').replace(',',''))
df['disliked'] = df['disliked'].apply(lambda x: x.replace('[','').replace(']','').replace('\'','').replace(',',''))

# Connect to the database
mydb = mysql.connector.connect(
  host="localhost",
  user="RobbeF",
  password="robbe",
  database="brewify"
)

# Fill up the users table in the database, column one: user_name, column two: style_preference, column three:
# style_dislike
mycursor = mydb.cursor()

for i in range(len(df)):
    sql = "INSERT INTO users (user_name, style_preference, style_dislike) VALUES (%s, %s, %s)"
    val = (df['username'][i], df['preference'][i], df['disliked'][i])
    mycursor.execute(sql, val)

mydb.commit()
mycursor.close()
mydb.close()
