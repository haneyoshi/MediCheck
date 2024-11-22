import mysql.connector
from ConnectDatabase import connection_pool

def cursorRead(query, params=None):
    try:
        connection = connection_pool.get_connection()
        myCursor = connection.cursor(dictionary=True)  # Use dictionary=True for better output formatting
        if params:
            myCursor.execute(query, params)
        else:
            myCursor.execute(query)
        results = myCursor.fetchall()
        print(f"Query Executed: {query} with Params: {params}")
        return results
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        myCursor.close()
        connection.close()