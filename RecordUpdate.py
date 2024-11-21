import mysql.connector
from ConnectDatabase import connection_pool

def cursorUpdate(formula, entry):
    try:
        connection = connection_pool.get_connection()
        myCursor = connection.cursor()
        myCursor.execute(formula, entry)
        print(f"Execute: {formula} with {entry}")
        connection.commit()
        return myCursor.rowcount  # Return the number of affected rows
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
    finally:
        myCursor.close()
        connection.close()
