import pandas as pd
from InsertionFormula import insert_visit, insert_disease, insert_medicine, insert_symptom, insert_prescription, insert_visitSymptom, insert_prescribedMedicine

# Read CSV file into DataFrame
csv_file = 'RandomClinicVisitData.csv'
df = pd.read_csv(csv_file)

# Iterate through each row of the DataFrame and insert data into the database
for _, row in df.iterrows():
    # Extract the data from the DataFrame row
    patient_id = row['patientID']
    visit_date = row['visit_date']
    symptoms = row['symptoms'].split(', ')
    diagnosed_disease = row['diagnosed_disease']
    prescribed_medicines = row['prescribed_medicines'].split(', ')

    # Insert visit data
    visit_id = insert_visit(patient_id,visit_date)  # Insert visit data, returning visit_id

    # Insert symptoms and link to visit
    for symptom_name in symptoms:
        insert_visitSymptom(visit_id, symptom_name)  # Insert each symptom associated with this visit

    # Insert disease and link to visit
    prescription_id = insert_prescription(visit_id, diagnosed_disease)  # Insert disease and create prescription record

    # Insert medicines and link to prescription
    for medicine_name in prescribed_medicines:
        insert_prescribedMedicine(prescription_id, medicine_name)  # Insert each medicine for the given prescription

print("Data insertion complete!")