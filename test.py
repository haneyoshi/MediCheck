import mysql.connector
connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mySQL20!",
  # database="MediDatabase"
)

myCursor = connection.cursor()
myCursor.execute("CREATE DATABASE MediDatabase")


# mysql -u root -p
# mysql_native_password.so
# plugin_dir    | /usr/local/mysql/lib/plugin/ 

# sudo brew services start mysql