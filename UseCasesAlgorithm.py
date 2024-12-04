from ClinicState import ClinicState
from Patient import Patient
import InsertionFormula


def patient_case_complete(patient: Patient, symptoms, disease, medicines):
    visit_id = InsertionFormula.insert_visit(patient.id)
    InsertionFormula.insert_visitSymptom(visit_id,symptoms)
    prescription_id = InsertionFormula.insert_prescription(visit_id,disease)
    InsertionFormula.insert_prescribedMedicine(prescription_id,medicines)
    print(f"patient's visit record achive{patient}")

def find_most_frequent_co_occurring_symptoms(symptom_name_list):
    print("find")

def find_most_possible_disease(symptom_list):
    print("find")

def find_possible_medicines(symptom_list):
    print("find")