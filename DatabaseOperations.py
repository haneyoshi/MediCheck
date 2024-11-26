import mysql.connector
from ConnectDatabase import connection_pool

# This function is used to handle data insertions, reads, updates, and deletions.
def execute_query(query, params=None):
    try:
        connection = connection_pool.get_connection()
        myCursor = connection.cursor(dictionary=True)
        # Use dictionary=True to get better formatted output when reading

        # Execute the query with or without parameters
        if params:
            myCursor.execute(query, params)
        else:
            myCursor.execute(query)
        
        print(f"Execute: {query} with Params: {params}")

        # If the query is a SELECT, fetch the results
        if query.strip().upper().startswith("SELECT"):
            results = myCursor.fetchall()
            return results

        # For INSERT, UPDATE, or DELETE, commit the changes and return the affected row count or last inserted ID
        connection.commit()
        if query.strip().upper().startswith("INSERT"):
            return myCursor.lastrowid
        else:
            return myCursor.rowcount

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
        # rollback():ensures that incomplete or invalid operations don’t affect the database.
    finally:
        myCursor.close()
        connection.close()

# a helper function to check if a value already exists
def get_or_insert(table_name, column_name, value):
    # Step 1: Check if value already exists in the table
    check_formula = f"SELECT {column_name}_id FROM {table_name} WHERE {column_name}_name = %s"
    result = execute_query(check_formula, (value,))
    if result:
        return result[0][f"{column_name}_id"]

    # Step 2: If it doesn't exist, insert the value
    insert_formula = f"INSERT INTO {table_name}({column_name}_name) VALUES(%s)"
    return execute_query(insert_formula, (value,))