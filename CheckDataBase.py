import mysql.connector

#create python and mySQL connection
db = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "mySQL20!",
  #database = "MediDataBase"
)

myCursor = db.cursor()

#check database exists
myCursor.execute("SHOW DATABASES")
d = "MediDataBase"
if not d in myCursor:
  myCursor.execute("CREATE DATABASE MediDatabase") 

  
