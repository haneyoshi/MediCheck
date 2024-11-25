import Patient
import Medicine
import Disease
import VisitRecord
import Symptom
import ReadFormula

def get_patient_profile(patient_id):
    # patient = (patient_id, first_name, last_name, date_of_birth)
    patient_data = ReadFormula.fetch_patient_by_id(patient_id)
    if not patient_data:
        raise ValueError(f"No patient found with given id:{patient_id}")
    
    # visit = (visit_id, visit_date)
    visit_data = ReadFormula.fetch_visits_by_patient_id(patient_id)
    visits= []
    for v in visit_data:
        visit_id, visit_date = v
        # symptom = (symptom_id, symptom_name)
        symptom_data = ReadFormula.fetch_symptoms_by_visit_id(visit_id)
        symptoms = [Symptom(**symptom) for symptom in symptom_data]
        # prescription = (prescription_id)
        prescription_data = ReadFormula.fetch_prescriptions_by_visit_id(visit_id)
        # disease = (disease_id, disease_name)
        disease_data = ReadFormula.fetch_disease_by_prescription_id(prescription_data[0])
        disease = Disease(disease_id=disease_data[0], disease_name = disease_data[1])
        # medicine = (medicine_id, medicine_name)
        medicine_data = ReadFormula.fetch_medicines_by_prescription_id(prescription_data[0])
        medicines = [Medicine(**medicine) for medicine in medicine_data]
        visit = VisitRecord(date=visit_date,visit_id=visit_id,diagnosed_disease=disease)
        visit.prescribed_medicines = medicines
        visit.reported_symptoms = symptoms
        visits.append(visit)

    
    patient = Patient(id=patient_data[0],fName=patient_data[1],lName=patient_data[2],dBirth=patient_data[3],history=visits)

    return patient

