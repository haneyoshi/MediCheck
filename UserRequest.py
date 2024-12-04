from Patient import Patient
# no need to refer the module prefix => Patient.Patient(patient_id=1, name="Alice")
import InsertionFormula
import PipeLineObject
from ClinicState import ClinicState
from UseCasesInteration import Diagnosing
import UseCasesAlgorithm

# instance to start take patient for a day
clinic_state = ClinicState()

def program_start():
    clinic_state.update_top_common_symptoms()

def patient_check_in():
    while True:
        user_input = input("Enter patient ID or type 'new' to create a new patient: ").strip()
        
        if user_input.lower() == 'new':
            new_patient = create_new_patient()  # Implement your create_new_patient function
            print(f"New patient created: {new_patient}")
            clinic_state.add_to_queue(new_patient)
            break

        try:
            patient = PipeLineObject.get_patient_profile(user_input)
            print(f"Patient retrieved: {patient}")
            clinic_state.add_to_queue(patient)
            break
        except ValueError as e:
            print(e)
            print("Please try again or type 'new' to create a new patient.")
            

def take_next_patien():
    # create instance to store user inputs
    diagnosing = Diagnosing()
    while True:  # Outer loop for the patient process
        print("\nProcessing next patient...")
        print(f"\nPatietn:{clinic_state.current_patient}")
        print(f"\ncommon symptoms of recent patients:{clinic_state.recent_top_common_symptoms}")
        diagnosing.taking_repoted_symptoms()
        diagnosing.giving_diagnosed_disease()
        diagnosing.prescribing_medicines()

        # Confirm and Break Outer Loop
        # print out summary
        diagnosing.diagnose_summary()
        confirm = input("\nConfirm this entry? (yes/no): ").strip().lower()
        if confirm == 'yes':
            print("Patient process completed.")
            break
        else:
            print("Restarting input for this patient...")
    patient = pateint_dequeue()
    UseCasesAlgorithm.patient_case_complete(patient, diagnosing.reported_symptoms, diagnosing.diagnosed_disease, diagnosing.prescribed_medicines)

def pateint_dequeue():
    # return the first patient in queue
    return clinic_state.pateint_dequeue()

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