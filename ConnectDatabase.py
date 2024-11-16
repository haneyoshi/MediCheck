from mysql.connector import pooling
#A connection pool maintains a pool of database connections that can be reused across operations.
# this module responsible for initializing the connection pool when your program starts.

#Connect the database
connection_pool = pooling.MySQLConnectionPool(
  pool_name="clinic_pool",
  pool_size=5, #number of connections in the pool
  host="localhost",
  user="root",
  password="mySQL20!",
  database="MediDataBase"
)