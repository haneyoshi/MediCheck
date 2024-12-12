from DatabaseOperations import execute_query
from InsertionFormula import insert_patient
from InsertionFormula import insert_visit, insert_disease, insert_medicine, insert_symptom, insert_prescription, insert_visitSymptom, insert_prescribedMedicine
import pandas as pd
import csv

def insert_random_patients(csv_file='RandomPatients.csv'):
    """
    Inserts random patient data from a CSV file into the database.
    """
    with open(csv_file, 'r') as file:
        file_reader = csv.reader(file)
        next(file_reader)  # Skip the header

        for line in file_reader:
            patient = (line[0], line[1], line[2], line[3])
            insert_patient(patient)

    print("Random patient data insertion complete!")

def insert_random_clinic_visits(csv_file='RandomClinicVisitData.csv'):
    """
    Inserts random clinic visit data from a CSV file into the database.
    """
    df = pd.read_csv(csv_file)

    for _, row in df.iterrows():
        patient_id = row['patientID']
        visit_date = row['visit_date']
        symptoms = row['symptoms'].split(', ')
        diagnosed_disease = row['diagnosed_disease']
        prescribed_medicines = row['prescribed_medicines'].split(', ')

        # Insert visit data
        visit_id = insert_visit(patient_id, visit_date)

        # Insert symptoms and link to visit
        for symptom_name in symptoms:
            insert_visitSymptom(visit_id, symptom_name)

        # Insert disease and link to visit
        prescription_id = insert_prescription(visit_id, diagnosed_disease)

        # Insert medicines and link to prescription
        for medicine_name in prescribed_medicines:
            insert_prescribedMedicine(prescription_id, medicine_name)

    print("Random clinic visit data insertion complete!")

def main():
    # Allow users to directly populate the database with random data

    # Scenario 1: Insert random patient data
    insert_random_patients()

    # Scenario 2: Insert random clinic visit data
    insert_random_clinic_visits()

    print("Random data population complete! You can now explore the program functionalities.")

if __name__ == "__main__":
    main()