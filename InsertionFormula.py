from DatabaseOperations import get_or_insert,execute_query

# Insert patient and return patient_id
# patient = (patient_id, first_name, last_name, date_of_birth)
def insert_patient(patient):
    table_name = "Patient"
    additional_values = {
        "patient_id": patient["patient_id"],
        "first_name": patient["first_name"],
        "last_name": patient["last_name"],
        "date_of_birth": patient["date_of_birth"],
    }
    return get_or_insert(table_name, "patient_id", patient["patient_id"], additional_values)

# Insert disease and return disease_id
def check_diease_exists(disease_name):
    return get_or_insert("Disease", "disease", disease_name)

# Insert medicine and return medicine_id
def check_medicine_exists(medicine_name):
    return get_or_insert("Medicine", "medicine", medicine_name)

# Insert symptom and return symptom_id
def check_symptom_exists(symptom_name):
    return get_or_insert("Symptom", "symptom", symptom_name)

# Insert visit and return visit_id
def insert_visit(patient_id):
    visitFormula = "INSERT INTO Visit(patient_id) VALUES(%s)"
    return_visit_id = execute_query(visitFormula, (patient_id,))
    if not return_visit_id:
        raise ValueError(f"***return_visit_id: {return_visit_id}, no return value found ")
    return execute_query(visitFormula, (patient_id,))

# Insert prescription and link it to the visit and disease
def insert_prescription(visit_id, disease_name):
    return_disease_id = check_diease_exists(disease_name)
    if not return_disease_id:
        raise ValueError(f"***return_visit_id: {return_disease_id}, no return value found ")
    prescriptionFormula = "INSERT INTO Prescription(visit_id, disease_id) VALUES(%s, %s)"
    return execute_query(prescriptionFormula, (visit_id, return_disease_id))

# Insert symptom for the visit
def insert_visitSymptom(visit_id, symptom_name):
    return_symptom_id = check_symptom_exists(symptom_name)
    if not return_symptom_id:
        raise ValueError(f"***return_symptom_id: {return_symptom_id}, no return value found ")
    visitSymptomFormula = "INSERT INTO VisitSymptom(visit_id, symptom_id) VALUES(%s, %s)"
    return execute_query(visitSymptomFormula, (visit_id, return_symptom_id))

# Insert prescribed medicine for the prescription
def insert_prescribedMedicine(prescription_id, medicine_name):
    return_medicine_id = check_medicine_exists(medicine_name)
    if not return_medicine_id:
        raise ValueError(f"***return_visit_id: {return_medicine_id}, no return value found ")
    prescribedMedicineFormula = "INSERT INTO PrescribedMedicine(prescription_id, medicine_id) VALUES(%s, %s)"
    return execute_query(prescribedMedicineFormula, (prescription_id, return_medicine_id))