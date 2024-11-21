# RecordDeletion module is resposible for connecting the database server to execute data deletion instruction
import mysql.connector
from ConnectDatabase import connection_pool

def cursorDeletion(formula, entry):
    try:
        connection = connection_pool.get_connection()
        myCursor = connection.cursor()
        myCursor.execute(formula, entry)
        print(f"Execute: {entry}")
        connection.commit()
        return myCursor.rowcount  # Return the number of rows deleted
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
    finally:
        myCursor.close()
        connection.close()