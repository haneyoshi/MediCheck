# DeletionFormula module contains pre-dfined methods that take input parameter to format data deletion instruction and then pass the other module, DatabaseOperations
from DatabaseOperations import execute_query

def delete_patient(patient_id):
    patientFormula = "DELETE FROM Patient WHERE patient_id = %s"
    # For insert_patient, the parameter patient is expected to be a tuple containing multiple values, e.g., ('P001', 'John', 'Doe', '1990-01-01'). These values map directly to the placeholders (%s) in the VALUES part of the SQL statement.
    # While, delete_patient, the parameter patient_id is a single value (e.g., 'P001').In Python, when passing a single value to a parameterized query, you must wrap it in a tuple. The syntax (patient_id,) creates a tuple with one element. Without the comma, Python would interpret it as a string, not a tuple, which would cause an error.
    return execute_query(patientFormula, (patient_id,))

def delete_disease(disease_id):
    diseaseFormula = "DELETE FROM Disease WHERE disease_id = %s"
    return execute_query(diseaseFormula, (disease_id,))

def delete_medicine(medicine_id):
    medicineFormula = "DELETE FROM Medicine WHERE medicine_id = %s"
    return execute_query(medicineFormula, (medicine_id,))

def delete_symptom(symptom_id):
    symptomFormula = "DELETE FROM Symptom WHERE symptom_id = %s"
    return execute_query(symptomFormula, (symptom_id,))

def delete_visit(visit_id):
    visitFormula = "DELETE FROM Visit WHERE visit_id = %s"
    return execute_query(visitFormula, (visit_id,))

def delete_prescription(prescription_id):
    prescriptionFormula = "DELETE FROM Prescription WHERE prescription_id = %s"
    return execute_query(prescriptionFormula, (prescription_id,))

def delete_visitSymptom(visit_symptom_id):
    visitSymptomFormula = "DELETE FROM VisitSymptom WHERE visit_symptom_id = %s"
    return execute_query(visitSymptomFormula, (visit_symptom_id,))

def delete_prescribedMedicine(prescribed_medicine_id):
    prescribedMedicineFormula = "DELETE FROM PrescribedMedicine WHERE medicine_id = %s"
    return execute_query(prescribedMedicineFormula, (prescribed_medicine_id,))