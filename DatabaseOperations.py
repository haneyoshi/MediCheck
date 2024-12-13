import mysql.connector
from ConnectDatabase import get_connection

# This function is used to handle data insertions, reads, updates, and deletions.
def execute_query(query, params=None):
    """
    Execute a query using a direct database connection.
    """
    connection = None
    cursor = None
    try:
        # Get a connection
        connection = get_connection()
        cursor = connection.cursor(buffered=True, dictionary=True)
        print(f"\n***Executing Query:\n{query} \nwith Params: {params}\n") 

        # Execute the query
        if params:
            print("Executing query with parameters.")
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        # If the query is a SELECT, fetch results
        if query.strip().upper().startswith("SELECT") or "WITH" in query.strip().upper():
            print("Fetching results for SELECT query.")
            results = cursor.fetchall()
            print(f"\nQuery Results: {results}")
            return results

        # Commit for non-SELECT queries
        connection.commit()
        if query.strip().upper().startswith("INSERT"):
            return cursor.lastrowid
        else:
            return cursor.rowcount
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        if connection:
            connection.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
            print("Cursor closed.")
        if connection:
            connection.close()
            print("Connection closed.")


# a helper function to check if a value already exists
def get_or_insert(table_name, column_name, value, additional_values=None):
    """
    A helper function to check if a record exists, and insert if not.
    Handles tables with and without auto-generated IDs.
    """
    if additional_values is None:
        additional_values = {}

    # Step 1: Check if the value exists
    check_formula = f"SELECT {column_name}_id FROM {table_name} WHERE {column_name}_name = %s"
    result = execute_query(check_formula, (value,))
    if result:
        return result[0][f"{column_name}_id"]

    # Step 2: Insert if it doesn't exist
    if not additional_values:
        # For tables with only one column value
        insert_formula = f"INSERT INTO {table_name}({column_name}_name) VALUES(%s)"
        return execute_query(insert_formula, (value,))
    else:
        # For tables like Patient, where multiple columns need to be inserted
        column_names = ", ".join(additional_values.keys())
        placeholders = ", ".join(["%s"] * len(additional_values))
        insert_formula = f"INSERT INTO {table_name}({column_names}) VALUES({placeholders})"
        return execute_query(insert_formula, tuple(additional_values.values()))