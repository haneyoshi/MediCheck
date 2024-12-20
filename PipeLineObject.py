from Patient import Patient
from Medicine import Medicine
from Disease import Disease
from VisitRecord import VisitRecord
from Symptom import Symptom
import ReadFormula

def get_patient_profile(patient_id):
    print("*** 'get_patient_profile' is called ")
    # patient = (patient_id, first_name, last_name, date_of_birth)
    patient_data = ReadFormula.fetch_patient_by_id(patient_id)
    print(f"Fetch the patient profile from database{patient_data}\n")
    if not patient_data:
        raise ValueError(f"No patient found with given id:{patient_id}")
    patient_data = patient_data[0]
    # Extract the first (and only) result, result returned from executing a query is always a "list" of dictionaries, buy explicitly refering to the index(e.g. [0] ) to access the element


    # Create patient object
    patient = Patient(patient_id=patient_data["patient_id"],first_name=patient_data["first_name"],last_name=patient_data["last_name"],date_of_birth=patient_data["date_of_birth"])
    print(f"*** create a Patient object {patient}\n")
    # Fetch visits
    visit_data = ReadFormula.fetch_visits_by_patient_id(patient_id)
    print(f"*** Fetch patient's visit data: {visit_data}\n")
    if visit_data:
        visits= []
        for v in visit_data:
            visit_id = v['visit_id']  # Access dictionary keys explicitly
            visit_date = v['visit_date']
            print(f"*** Processing Visit ID: {v['visit_id']}, Visit Date: {v['visit_date']}\n")

            # Fetch symptoms
            symptom_data = ReadFormula.fetch_symptoms_by_visit_id(int(visit_id))
            print(f"*** symptoms under visit id {v['visit_id']}: {symptom_data}\n")
            symptoms = [Symptom(**symptom) for symptom in symptom_data]
            # Iterate through the list to process each dictionary

            # Fetch prescriptions
            prescription_data = ReadFormula.fetch_prescriptions_by_visit_id(visit_id)
            if not prescription_data:
                raise ValueError(f"No prescription found for visit ID: {visit_id}")
            prescription_record = prescription_data[0]
            prescription_id = prescription_record["prescription_id"]
            disease_id = prescription_record["disease_id"]
            print(f"*** Prescriptions for Visit ID {visit_id}: {prescription_id}\n")
            
            # Fetch diseases
            # disease_data = ReadFormula.fetch_disease_by_prescription_id(prescription_id)
            # if not disease_data:
            diease_name = ReadFormula.fetch_disease_by_id(disease_id)
            if not diease_name:
                raise ValueError(f"no diease_name found for id: {disease_id}")
            #     raise ValueError(f"No disease found for prescription ID: {prescription_id}")
            # print(f"\nDisease Data: {disease_data}")
            disease = Disease(disease_id=disease_id, disease_name = diease_name)

            # Fetch medicines
            medicine_data = ReadFormula.fetch_medicines_by_prescription_id(prescription_id)
            print(f"\nFetch prescribed medicine under P_id {prescription_id}: {medicine_data}")
            medicines = [Medicine(**medicine) for medicine in medicine_data]

            # Create visit record
            visit = VisitRecord(date=visit_date,visit_id=visit_id,diagnosed_disease=disease)
            visit.prescribed_medicines = medicines
            visit.reported_symptoms = symptoms
            visits.append(visit)
            patient.records=visits
    else:
        print("no visit record for this patient")
    return patient

def add_Patient_visit_to_instance(visit_id, patient:Patient):
    # visit = (visit_id, patient_id, date)
    visit_data = ReadFormula.fetch_visit_by_id(visit_id)
    if not visit_data:
        raise ValueError(f"No visit found for id: {visit_id}")
    visit_record = visit_data[0]
    visit_id = visit_record["visit_id"]
    # patient_id = visit_record["patient_id"]
    visit_date = visit_record["visit_date"]
    # symptom = (symptom_id, symptom_name)
    symptom_data = ReadFormula.fetch_symptoms_by_visit_id(visit_id)
    if not symptom_data:
        raise ValueError(f"no symptom found for id: visit id: {visit_id}")
    symptoms = [Symptom(**symptom) for symptom in symptom_data]
    # Iterate through the list to process each dictionary

    prescription_data = ReadFormula.fetch_prescriptions_by_visit_id(visit_id)
    if not prescription_data:
        raise ValueError(f"no prescription found for visit id: {visit_id}")
    prescription_record = prescription_data[0]
    prescription_id = prescription_record["prescription_id"]
    disease_id = prescription_record["disease_id"]
    disease_name = ReadFormula.fetch_disease_by_id(disease_id)
    if not disease_name:
        raise ValueError(f"no disease name found for disease id: {disease_id}")
    disease = Disease(disease_id=disease_id, disease_name = disease_name)
    # medicine = (medicine_id, medicine_name)
    medicine_data = ReadFormula.fetch_medicines_by_prescription_id(prescription_id)
    if not medicine_data:
        raise ValueError(f"no medicine name found for precription id: {prescription_id}")
    medicines = [Medicine(**medicine) for medicine in medicine_data]
    visit = VisitRecord(date=visit_date,visit_id=visit_id,diagnosed_disease=disease)
    visit.prescribed_medicines = medicines
    visit.reported_symptoms = symptoms
    patient.records.append(visit)

def coocurring_symptom_instance(symptom_data):
    if not symptom_data:  # Handles None or empty
        print("No symptom data found.")
        return []

    # Map fields from query results to Symptom class attributes
    symptoms = []
    for symptom in symptom_data:
        try:
            symptom_instance = Symptom(
                symptom_id=symptom['co_symptom_id'],
                symptom_name=symptom['symptom_name']
            )
            symptoms.append(symptom_instance)
        except KeyError as e:
            print(f"Missing expected key in symptom data: {e}")
    return symptoms