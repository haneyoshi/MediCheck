# Class that store data of current diagnosing
import UseCasesAlgorithm
from Patient import Patient

class Diagnosing:
    def __init__(self):
        self.reported_symptoms = []
        self.diagnosed_disease = None
        self.prescribed_medicines = []

    def taking_repoted_symptoms(self):
    # Symptom Entry Loop
        while True:
            symptom_input = input("\n\nEnter a symptom (or type 'done' to finish): ").strip()
            if symptom_input.lower() == 'done':
                break
            self.reported_symptoms.append(symptom_input)
            suggested_symptoms = UseCasesAlgorithm.find_most_frequent_co_occurring_symptoms(self.reported_symptoms)
            print(f"\npossible co_occurring symptoms{suggested_symptoms}")
        print(f"\nSymptoms recorded: {self.reported_symptoms}")

    def giving_diagnosed_disease(self):
        # Diagnosis Entry
        suggested_disease = UseCasesAlgorithm.find_most_possible_disease(self.reported_symptoms)
        print(f"\n\npossible disease:{suggested_disease}")
        self.diagnosed_disease = input("\nEnter diagnosis: ").strip()
        print(f"\nDiagnosis recorded: {self.diagnosed_disease}")


    def prescribing_medicines(self):
        # Prescribed Medicines Loop
        suggested_medicines = UseCasesAlgorithm.find_relevant_medicines(self.reported_symptoms,self.diagnosed_disease)
        print(f"\n\npossible relevant medicines:{suggested_medicines}")
        while True:
            medicine_input = input("\nEnter a prescribed medicine (or type 'done' to finish): ").strip()
            if medicine_input.lower() == 'done':
                break
            self.prescribed_medicines.append(medicine_input)
        print(f"\nPrescribed medicines recorded: {self.prescribed_medicines}")
    
    def diagnose_summary(self):
        print(f"\n\nSummary for this patient:\nSymptoms: {self.reported_symptoms}\nDiagnosis: {self.diagnosed_disease}\nMedicines: {self.prescribed_medicines}")

    def complete_diagnose(self,patient: Patient):
        UseCasesAlgorithm.patient_case_complete(patient, self.reported_symptoms, self.diagnosed_disease, self.prescribed_medicines)