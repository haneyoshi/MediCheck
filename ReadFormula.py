from DatabaseOperations import execute_query

# Fetch specific patient
def fetch_patient_by_id(patient_id):
    query = "SELECT * FROM Patient WHERE patient_id = %s"
    return execute_query(query, (patient_id,))

# Fetch all patients
def fetch_all_patients():
    query = "SELECT * FROM Patient"
    return execute_query(query)

# Fetch visits for a specific patient
def fetch_visits_by_patient_id(patient_id):
    query = "SELECT Visit.visit_id, Visit.visit_date FROM Visit WHERE patient_id = %s"
    return execute_query(query, (patient_id,))

# Fetch a specific visit
def fetch_visit_by_id(visit_id):
    query = "SELECT * FROM Visit WHERE visit_id = %s"
    return execute_query(query, (visit_id,))

# Fetch all symptoms
def fetch_all_symptoms():
    query = "SELECT * FROM Symptom"
    return execute_query(query)

# Fetch symptoms for a specific visit
def fetch_symptoms_by_visit_id(visit_id):
    query = """
        SELECT Symptom.symptom_id, Symptom.symptom_name
        FROM VisitSymptom
        INNER JOIN Symptom ON VisitSymptom.symptom_id = Symptom.symptom_id
        WHERE VisitSymptom.visit_id = %s
    """
    return execute_query(query, (visit_id,))

# Fetch all medicines
def fetch_all_medicines():
    query = "SELECT * FROM Medicine"
    return execute_query(query)

# Fetch all diseases
def fetch_all_diseases():
    query = "SELECT * FROM Disease"
    return execute_query(query)

# Fetch prescriptions for a specific visit
def fetch_prescriptions_by_visit_id(visit_id):
    query = "SELECT prescription_id FROM Prescription WHERE visit_id = %s"
    return execute_query(query, (visit_id,))

# fetch diagnosed disease fpr a specifi presciption
def fetch_disease_by_prescription_id(prescription_id):
    query = """SELECT Disease.disease_id, Disease.disease_name
        FROM Prescription
        INNER JOIN Disease ON Prescription.disease_id = Disease.disease_id
        WHERE Prescription.prescription_id = %s
        """
    return execute_query(query,prescription_id)

# Fetch medicines for a specific prescription
def fetch_medicines_by_prescription_id(prescription_id):
    query = """
        SELECT Medicine.medicine_id, Medicine.medicine.name
        FROM PrescribedMedicine
        INNER JOIN Medicine ON PrescribedMedicine.medicine_id = Medicine.medicine_id
        WHERE PrescribedMedicine.prescription_id = %s
    """
    return execute_query(query, (prescription_id,))

# Fetch all data for a specific patient
def fetch_all_patient_data(patient_id):
    query = """
        SELECT Patient.*, Visit.*, Prescription.*, Disease.*, 
               Medicine.medicine_name, Symptom.symptom_name
        FROM Patient
        LEFT JOIN Visit ON Patient.patient_id = Visit.patient_id
        LEFT JOIN Prescription ON Visit.visit_id = Prescription.visit_id
        LEFT JOIN Disease ON Prescription.disease_id = Disease.disease_id
        LEFT JOIN PrescribedMedicine ON Prescription.prescription_id = PrescribedMedicine.prescription_id
        LEFT JOIN Medicine ON PrescribedMedicine.medicine_id = Medicine.medicine_id
        LEFT JOIN VisitSymptom ON Visit.visit_id = VisitSymptom.visit_id
        LEFT JOIN Symptom ON VisitSymptom.symptom_id = Symptom.symptom_id
        WHERE Patient.patient_id = %s;
    """
    return execute_query(query, (patient_id,))

# Fetch most common symptoms
def fetch_most_common_symptoms(limit=10):
    query = """
        SELECT Symptom.symptom_name, COUNT(*) AS frequency
        FROM VisitSymptom
        INNER JOIN Symptom ON VisitSymptom.symptom_id = Symptom.symptom_id
        GROUP BY Symptom.symptom_name
        ORDER BY frequency DESC
        LIMIT %s;
    """
    return execute_query(query, (limit,))

# Fetch most prescribed medicines
def fetch_most_prescribed_medicines(limit=10):
    query = """
        SELECT Medicine.medicine_name, COUNT(*) AS frequency
        FROM PrescribedMedicine
        INNER JOIN Medicine ON PrescribedMedicine.medicine_id = Medicine.medicine_id
        GROUP BY Medicine.medicine_name
        ORDER BY frequency DESC
        LIMIT %s;
    """
    return execute_query(query, (limit,))