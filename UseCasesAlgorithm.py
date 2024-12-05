from ClinicState import ClinicState
from Patient import Patient
import InsertionFormula
import ReadFormula
import PipeLineObject

def patient_case_complete(patient: Patient, symptoms, disease, medicines):
    visit_id = InsertionFormula.insert_visit(patient.id)
    InsertionFormula.insert_visitSymptom(visit_id,symptoms)
    prescription_id = InsertionFormula.insert_prescription(visit_id,disease)
    InsertionFormula.insert_prescribedMedicine(prescription_id,medicines)
    print(f"patient's visit record achive{patient}")
    add_new_record_to_Patient_instance(visit_id,patient)

def add_new_record_to_Patient_instance(visit_id,patient: Patient):
    #  store new record to local patient instance
    PipeLineObject.add_Patient_visit_to_instance(visit_id,patient)
    print(f"fetch local instance{patient}")

def find_most_frequent_co_occurring_symptoms(symptom_name_list):
    print("find")

def find_most_possible_disease(symptom_list):
    print("find")

def find_possible_medicines(symptom_list):
    print("find")