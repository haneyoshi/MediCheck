from DatabaseOperations import get_or_insert,execute_query

# Insert patient and return patient_id
# patient = (patient_id, first_name, last_name, date_of_birth)
def insert_patient(patient):
    patientFormula = """
        INSERT INTO Patient(patient_id, first_name, last_name, date_of_birth)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE patient_id = LAST_INSERT_ID(patient_id)
    """
    return get_or_insert(patientFormula, patient)

# Insert disease and return disease_id
def insert_disease(disease_name):
    return get_or_insert("Disease", "disease", disease_name)

# Insert medicine and return medicine_id
def insert_medicine(medicine_name):
    return get_or_insert("Medicine", "medicine", medicine_name)

# Insert symptom and return symptom_id
def insert_symptom(symptom_name):
    return get_or_insert("Symptom", "symptom", symptom_name)

# Insert visit and return visit_id
def insert_visit(patient_id):
    visitFormula = "INSERT INTO Visit(patient_id) VALUES(%s,%s)"
    return execute_query(visitFormula, (patient_id,))

# Insert prescription and link it to the visit and disease
def insert_prescription(visit_id, disease_name):
    disease_id = insert_disease(disease_name)
    prescriptionFormula = "INSERT INTO Prescription(visit_id, disease_id) VALUES(%s, %s)"
    return execute_query(prescriptionFormula, (visit_id, disease_id))

# Insert symptom for the visit
def insert_visitSymptom(visit_id, symptom_name):
    symptom_id = insert_symptom(symptom_name)
    visitSymptomFormula = "INSERT INTO VisitSymptom(visit_id, symptom_id) VALUES(%s, %s)"
    return execute_query(visitSymptomFormula, (visit_id, symptom_id))

# Insert prescribed medicine for the prescription
def insert_prescribedMedicine(prescription_id, medicine_name):
    medicine_id = insert_medicine(medicine_name)
    prescribedMedicineFormula = "INSERT INTO PrescribedMedicine(prescription_id, medicine_id) VALUES(%s, %s)"
    return execute_query(prescribedMedicineFormula, (prescription_id, medicine_id))