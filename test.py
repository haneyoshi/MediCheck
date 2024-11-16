import mysql.connector
connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mySQL20!",
  database="MediDatabase"
)

myCursor = connection.cursor()
myCursor.execute("SHOW TABLES")
for db in myCursor:
  print(db)

# mysql -u root -p
# mysql_native_password.so
# plugin_dir    | /usr/local/mysql/lib/plugin/ 

# sudo brew services start mysql