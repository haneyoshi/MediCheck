import os

import mysql.connector

# Configuration for database connection
DB_CONFIG = {
    "host": os.getenv("MEDICHECK_DB_HOST", "localhost"),
    "port": int(os.getenv("MEDICHECK_DB_PORT", "3306")),
    "user": os.getenv("MEDICHECK_DB_USER", "root"),
    "password": os.getenv("MEDICHECK_DB_PASSWORD", ""),
    "database": os.getenv("MEDICHECK_DB_NAME", "MediDatabase"),
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
