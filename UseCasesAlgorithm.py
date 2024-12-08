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
    # retrieve corresponding symptom ids
    co_occurring_symptoms = ReadFormula.fetch_most_possible_combinations_for_given_symptoms(symptom_name_list)
    # return symptom instance object list
    return PipeLineObject.coocurring_symptom_instance(co_occurring_symptoms)


def find_most_possible_disease(symptom_list):
    return ReadFormula.fetch_most_possible_disease_for_given_symptoms(symptom_list)

def find_relevant_medicines(symptom_list,disease):
    return ReadFormula.fetch_most_relevant_medicine_for_given_symptoms_and_disease(symptom_list,disease)