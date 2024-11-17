import mysql.connector
from mysql.connector import pooling

# Connection pool setup
connection_pool = pooling.MySQLConnectionPool(
    pool_name="clinic_pool",
    pool_size=5,
    host="localhost",
    user="root",
    password="mySQL20!",
    database="MediDatabase"
)

def create_tables():
    # SQL Statements for creating tables
    sql_statements = [
        """
        CREATE TABLE IF NOT EXISTS Patient (
            patient_id VARCHAR(10),
            first_name VARCHAR(20) NOT NULL,
            last_name VARCHAR(20) NOT NULL,
            date_of_birth DATE NOT NULL,
            PRIMARY KEY(patient_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Visit (
            visit_id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id VARCHAR(10),
            visit_date DATETIME,
            FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Symptom (
            symptom_id INT AUTO_INCREMENT PRIMARY KEY,
            symptom_name VARCHAR(50) NOT NULL,
            UNIQUE (symptom_name)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS VisitSymptom (
            visit_symptom_id INT AUTO_INCREMENT PRIMARY KEY,
            visit_id INT,
            symptom_id INT,
            FOREIGN KEY (visit_id) REFERENCES Visit(visit_id),
            FOREIGN KEY (symptom_id) REFERENCES Symptom(symptom_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Medicine (
            medicine_id INT AUTO_INCREMENT PRIMARY KEY,
            medicine_name VARCHAR(50) NOT NULL,
            UNIQUE (medicine_name)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Disease (
            disease_id INT AUTO_INCREMENT PRIMARY KEY,
            disease_name VARCHAR(50) NOT NULL,
            UNIQUE (disease_name)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Prescription (
            prescription_id INT AUTO_INCREMENT PRIMARY KEY,
            visit_id INT,
            disease_id INT,
            FOREIGN KEY (visit_id) REFERENCES Visit(visit_id),
            FOREIGN KEY (disease_id) REFERENCES Disease(disease_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS PrescribedMedicine (
            prescription_id INT,
            medicine_id INT,
            FOREIGN KEY (prescription_id) REFERENCES Prescription(prescription_id),
            FOREIGN KEY (medicine_id) REFERENCES Medicine(medicine_id)
        );
        """
    ]

    # Execute the statements
    try:
        # Get a connection from the pool
        connection = connection_pool.get_connection()
        cursor = connection.cursor()

        # Execute each statement
        for sql in sql_statements:
            cursor.execute(sql)
            print(f"Executed: {sql.splitlines()[1].strip()}")  # Log table creation
        
        # Commit changes
        connection.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

# Call the function to create tables
create_tables()