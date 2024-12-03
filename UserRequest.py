from Patient import Patient
# no need to refer the module prefix => Patient.Patient(patient_id=1, name="Alice")
import InsertionFormula
import PipeLineObject
import Symptom
from ClinicState import ClinicState

def program_start():
    ClinicState.update_top_common_symptoms

def patient_check_in():
    while True:
        user_input = input("Enter patient ID or type 'new' to create a new patient: ").strip()
        
        if user_input.lower() == 'new':
            new_patient = create_new_patient()  # Implement your create_new_patient function
            print(f"New patient created: {new_patient}")
            ClinicState.add_to_queue(new_patient)
            break

        try:
            patient = PipeLineObject.get_patient_profile(user_input)
            print(f"Patient retrieved: {patient}")
            ClinicState.add_to_queue(patient)
            break
        except ValueError as e:
            print(e)
            print("Please try again or type 'new' to create a new patient.")
            

def take_next_patien():
    while True:  # Outer loop for the patient process
        print("\nProcessing next patient...")

        # Symptom Entry Loop
        symptoms = []
        while True:
            symptom_input = input("Enter a symptom (or type 'done' to finish): ").strip()
            if symptom_input.lower() == 'done':
                break
            symptoms.append(symptom_input)
        print(f"Symptoms recorded: {symptoms}")

        # Diagnosis Entry
        diagnosis = input("Enter diagnosis: ").strip()
        print(f"Diagnosis recorded: {diagnosis}")

        # Prescribed Medicines Loop
        medicines = []
        while True:
            medicine_input = input("Enter a prescribed medicine (or type 'done' to finish): ").strip()
            if medicine_input.lower() == 'done':
                break
            medicines.append(medicine_input)
        print(f"Prescribed medicines recorded: {medicines}")

        # Confirm and Break Outer Loop
        print(f"\nSummary for this patient:\nSymptoms: {symptoms}\nDiagnosis: {diagnosis}\nMedicines: {medicines}")
        confirm = input("Confirm this entry? (yes/no): ").strip().lower()
        if confirm == 'yes':
            print("Patient process completed.")
            break
        else:
            print("Restarting input for this patient...")
    

def pateint_dequeue():
    # return the first patient in queue
    return ClinicState.pateint_dequeue()

def create_new_patient():
    print("Creating a new patient...")
    patient_id = input("Enter patient ID: ").strip()
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name: ").strip()
    date_of_birth = input("Enter date of birth (YYYY-MM-DD): ").strip()
    patient_data = (patient_id,first_name,last_name,date_of_birth)
    new_record = InsertionFormula.insert_patient(patient_data)
    print(f"new patient record{new_record}")
    patient = Patient(id=patient_id,fName=first_name,lName=last_name,dBirth=date_of_birth)
    return patient