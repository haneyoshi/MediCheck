from ConnectDatabase import get_connection
from DatabaseOperations import get_or_insert, execute_query

# Insert patient and return patient_id
# patient = (patient_id, first_name, last_name, date_of_birth)
def insert_patient(patient):
    formula = """
        INSERT INTO Patient(patient_id, first_name, last_name, date_of_birth)
        VALUES(%s, %s, %s, %s)
    """
    result = execute_query(formula, (
        patient["patient_id"], patient["first_name"], patient["last_name"],
        patient["date_of_birth"],
    ))
    # Patient uses a VARCHAR primary key, so MySQL may report lastrowid as 0
    # even when the INSERT succeeded. Only None represents helper failure.
    if result is None:
        raise RuntimeError("Patient registration was not saved.")
    return patient["patient_id"]

# Insert disease and return disease_id
def check_diease_exists(disease_name, connection=None):
    return get_or_insert("Disease", "disease", disease_name, connection=connection)

# Insert medicine and return medicine_id
def check_medicine_exists(medicine_name, connection=None):
    return get_or_insert("Medicine", "medicine", medicine_name, connection=connection)

# Insert symptom and return symptom_id
def check_symptom_exists(symptom_name, connection=None):
    return get_or_insert("Symptom", "symptom", symptom_name, connection=connection)

# Insert visit and return visit_id
def insert_visit(patient_id, connection=None, visit_date=None):
    if visit_date:
        visitFormula = "INSERT INTO Visit(patient_id, visit_date) VALUES(%s, %s)"
        params = (patient_id, visit_date)
    else:
        visitFormula = "INSERT INTO Visit(patient_id) VALUES(%s)"
        params = (patient_id,)
    return_visit_id = execute_query(visitFormula, params, connection=connection)
    if not return_visit_id:
        raise ValueError(f"***return_visit_id: {return_visit_id}, no return value found ")
    return return_visit_id

# Insert prescription and link it to the visit and disease
def insert_prescription(visit_id, disease_name, connection=None):
    return_disease_id = check_diease_exists(disease_name, connection=connection)
    if not return_disease_id:
        raise ValueError(f"***return_visit_id: {return_disease_id}, no return value found ")
    prescriptionFormula = "INSERT INTO Prescription(visit_id, disease_id) VALUES(%s, %s)"
    return execute_query(prescriptionFormula, (visit_id, return_disease_id), connection=connection)

# Insert symptom for the visit
def insert_visitSymptom(visit_id, symptom_name, connection=None):
    return_symptom_id = check_symptom_exists(symptom_name, connection=connection)
    if not return_symptom_id:
        raise ValueError(f"***return_symptom_id: {return_symptom_id}, no return value found ")
    visitSymptomFormula = "INSERT INTO VisitSymptom(visit_id, symptom_id) VALUES(%s, %s)"
    return execute_query(visitSymptomFormula, (visit_id, return_symptom_id), connection=connection)

# Insert prescribed medicine for the prescription
def insert_prescribedMedicine(prescription_id, medicine_name, connection=None):
    return_medicine_id = check_medicine_exists(medicine_name, connection=connection)
    if not return_medicine_id:
        raise ValueError(f"***return_visit_id: {return_medicine_id}, no return value found ")
    prescribedMedicineFormula = "INSERT INTO PrescribedMedicine(prescription_id, medicine_id) VALUES(%s, %s)"
    return execute_query(prescribedMedicineFormula, (prescription_id, return_medicine_id), connection=connection)


def insert_complete_consultation(patient_id, symptoms, disease, medicines, visit_date=None):
    """Persist every record belonging to one consultation in one transaction."""
    connection = get_connection()
    try:
        connection.start_transaction()
        if visit_date:
            visit_id = insert_visit(patient_id, connection=connection, visit_date=visit_date)
        else:
            visit_id = insert_visit(patient_id, connection=connection)
        for symptom in symptoms:
            insert_visitSymptom(visit_id, symptom, connection=connection)
        prescription_id = insert_prescription(visit_id, disease, connection=connection)
        for medicine in medicines:
            insert_prescribedMedicine(prescription_id, medicine, connection=connection)
        connection.commit()
        return visit_id
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
