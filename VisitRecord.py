# class VisitRecord
import Medicine
import Symptom
import Disease
class VisitRecord:
    def __init__(self,date,visit_id,diagnosed_disease: Disease):
        self.date = date
        self.visit_id = visit_id
        self.diagnosed_disease = diagnosed_disease
        self.prescribed_medicines =[]
        self.reported_symptoms = []

  # Method to add a medicine
    def add_prescribed_medicine(self, medicine):
        if not isinstance(medicine, Medicine) or not medicine:
            raise ValueError("medicine must be a Medicine Object")
        self.prescribed_medicines.append(medicine)

    # Method to remove a medicine
    def remove_prescribed_medicine(self, medicine):
        if medicine in self.prescribed_medicines:
            self.prescribed_medicines.remove(medicine)
        else:
            raise ValueError(f"Medicine '{medicine}' not found")

    # Method to display all medicines
    def list_prescribed_medicines(self):
        return self.prescribed_medicines
    
     # Method to add a symptom
    def add_reported_symptom(self, symptom):
        if not isinstance(symptom, Symptom) or not symptom:
            raise ValueError("symptom must be a Symptom Object")
        self.reported_symptoms.append(symptom)

    # Method to remove a symptom
    def remove_reported_symptom(self, symptom):
        if symptom in self.reported_symptoms:
            self.reported_symptoms.remove(symptom)
        else:
            raise ValueError(f"Symptom '{symptom}' not found")

    # Method to display all symptom
    def list_reported_symptoms(self):
        return self.reported_symptoms

    def __eq__(self, other):
        if not isinstance(other,VisitRecord):
            return NotImplemented
        return self.date == other.date

    def __repr__(self):
        return f"Record(date={self.date}, diagnosed_disease={self.diagnosed_disease}, symptoms={self.reported_symptoms},medicines={self.prescribed_medicines})"