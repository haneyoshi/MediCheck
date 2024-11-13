import mysql.connector

#Connect the database
db=mysql.connector.connect(
  host="localhost",
  user="root",
  password="mySQL20!",
  database="MediDataBase"
)

# myCursor=db.cursor()