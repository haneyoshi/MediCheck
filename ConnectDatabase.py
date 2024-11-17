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
  database="MediDatabase"
  # auth_plugin='mysql_native_password'
)

def connect_pool(instruction):
  try:
    connect = connection_pool.get_connection()
    myCursor = connect.cursor()
    print("execute show tables")
    myCursor.execute(instruction)
    tables = myCursor.fetchall()
    return tables
  finally:
    myCursor.close()
    connect.close()


def get_tables():
  instruction = "SHOW TABLES"
  output(connect_pool(instruction))

def output(out_put_content):
  for content in out_put_content:
    print(content)