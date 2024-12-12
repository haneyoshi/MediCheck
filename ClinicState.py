#Encapsulation in a Class
from Patient import Patient
import ReadFormula
from Symptom import Symptom

class ClinicState:
    def __init__(self):
        self.recent_top_common_symptoms = []
        self.current_patient = None
        self.in_queue = []
        self.patients_visit_today = []

    def update_top_common_symptoms(self):
        # symptom = (symptom_id, symptom_name,frequency)
        symptom_data = ReadFormula.fetch_most_common_symptoms()
        if symptom_data is None or len(symptom_data) == 0:
            print("\nNo data retrieved for common symptoms.")
            return  # Avoid processing None or empty data
        self.recent_top_common_symptoms = [Symptom(symptom_id=symptom['symptom_id'], symptom_name=symptom['symptom_name']) for symptom in symptom_data]

    def set_current_patient(self, patient):
        self.current_patient = patient

    # def document_patient_visit(self):
    #     self.current_patient = self.pateint_dequeue()

    def add_to_queue(self, patient:Patient):
        self.in_queue.append(patient)

    def next_in_queue(self) ->Patient:
        # return the first value in list
        self.current_patient = self.in_queue.pop(0)
        print(f"current serving patient{self.current_patient}")
        self.patients_visit_today.append(self.current_patient)
        return self.current_patient
    
    def patient_dequeue(self):
        patient = self.in_queue.pop(0)
        print(f"patient leave: {patient}")