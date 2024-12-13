# Class that store data of current diagnosing

class Diagnosing:
    def __init__(self):
        self.reported_symptoms = []
        self.diagnosed_disease = None
        self.prescribed_medicines = []
    
    def diagnose_summary(self):
        return (f"\n\nSummary for this patient:\nSymptoms: {self.reported_symptoms}\nDiagnosis: {self.diagnosed_disease}\nMedicines: {self.prescribed_medicines}")

    def case_reset(self):
        self.reported_symptoms = []
        self.diagnosed_disease = None
        self.prescribed_medicines = []

    def __repr__(self):
        return f"Symptoms: {self.reported_symptoms},\nDignose {self.diagnosed_disease}, \nPrescription: {self.prescribed_medicines}"