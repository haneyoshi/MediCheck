#Encapsulation in a Class
from Patient import Patient
import ReadFormula
import Symptom

class ClinicState:
    def __init__(self):
        self.recent_top_common_symptoms = []
        self.current_patient = None
        self.in_queue = []
        self.patients_visit_today = []

    def update_top_common_symptoms(self):
        # symptom = (symptom_id, symptom_name)
        symptom_data = ReadFormula.fetch_most_common_symptoms()
        self.recent_top_common_symptoms = [Symptom(**symptom) for symptom in symptom_data]

    def set_current_patient(self, patient):
        self.current_patient = patient

    # def document_patient_visit(self):
    #     self.current_patient = self.pateint_dequeue()

    def add_to_queue(self, patient:Patient):
        self.in_queue.append(patient)

    def pateint_dequeue(self) ->Patient:
        # return the first value in list
        self.current_patient = self.in_queue.pop(0)
        self.patients_visit_today.append(self.current_patient)
        return self.current_patient