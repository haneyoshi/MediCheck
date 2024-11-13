import mysql.connector
db = mysql.connector.connect(
 host = "localhost",
 user ="root",
 password = "mySQL20!"
 database = "testdatabase"
)

mycursor = db.cursor()
#mycursor.execute("CREATE DATABASE testdatabase")
#create database to test whether success connecting to tadabase
