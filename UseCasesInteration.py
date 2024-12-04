# Class that store data of current diagnosing
class Diagnosing:
    def __init__(self):
        self.reported_symptoms = []
        self.diagnosed_disease = None
        self.prescribed_medicines = []

    def taking_repoted_symptoms(self):
    # Symptom Entry Loop
        while True:
            
            symptom_input = input("\nEnter a symptom (or type 'done' to finish): ").strip()
            if symptom_input.lower() == 'done':
                break
            self.reported_symptoms.append(symptom_input)
        print(f"\nSymptoms recorded: {self.reported_symptoms}")
        return self.reported_symptoms

    def giving_diagnosed_disease(self):
        # Diagnosis Entry
        self.diagnosed_disease = input("\nEnter diagnosis: ").strip()
        print(f"\nDiagnosis recorded: {self.diagnosed_disease}")
        return self.diagnosed_disease

    def prescribing_medicines(self):
        # Prescribed Medicines Loop
        while True:
            medicine_input = input("\nEnter a prescribed medicine (or type 'done' to finish): ").strip()
            if medicine_input.lower() == 'done':
                break
            self.prescribed_medicines.append(medicine_input)
        print(f"\nPrescribed medicines recorded: {self.prescribed_medicines}")
        return self.prescribed_medicines
    
    def diagnose_summary(self):
        print(f"\nSummary for this patient:\nSymptoms: {self.reported_symptoms}\nDiagnosis: {self.diagnosed_disease}\nMedicines: {self.prescribed_medicines}")