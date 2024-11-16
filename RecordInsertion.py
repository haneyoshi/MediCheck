from ConnectDatabase import connection_pool
# this module is called to check whether data instances exist, if not insert new record and return instance id, or staight return found record id

connection = connection_pool.get_connection()
myCursor=connection.cursor()

def cursorInsertion(action):
  try:
    myCursor.execute(action)
    connection.commit()
    return myCursor.lastrowid
    #return the id found or new record's id
  except Exception as e:
    print ("An error occured", e)
    connection.rollback()
    # rollback():ensures that incomplete or invalid operations don’t affect the database.
  finally:
    myCursor.close()
    connection.close()