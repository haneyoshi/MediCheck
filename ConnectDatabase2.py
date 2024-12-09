import mysql.connector

# Configuration for database connection
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "mySQL20!",
    "database": "MediDatabase",
}

def get_connection():
    """
    Establish a direct connection to the database.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("Database connection established.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        raise
