import Patient
import InsertionFormula
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