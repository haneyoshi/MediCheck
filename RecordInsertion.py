import mysql.connector
from ConnectDatabase import connection_pool
# this module is called to check whether data instances exist, if not insert new record and return instance id, or staight return found record id


def cursorInsertion(formula,entry):
  try:
    connection = connection_pool.get_connection()
    myCursor=connection.cursor()
    myCursor.execute(formula,entry)
    print(f"Execute: {entry}")
    connection.commit()
    return myCursor.lastrowid
    #return the id found or new record's id
  except mysql.connector.Error as err:
    print(f"Error: {err}")
    connection.rollback()
    # rollback():ensures that incomplete or invalid operations don’t affect the database.
  finally:
    myCursor.close()
    connection.close()