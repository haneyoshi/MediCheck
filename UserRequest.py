from Patient import Patient
# no need to refer the module prefix => Patient.Patient(patient_id=1, name="Alice")
import InsertionFormula
import PipeLineObject
from ClinicState import ClinicState
from UseCasesInteration import Diagnosing
import UseCasesAlgorithm

# instance to start take patient for a day
clinic_state = ClinicState()
diagnosing = Diagnosing()
def program_start():
    clinic_state.update_top_common_symptoms()

def patient_check_in(patient_id=None):
    """
    Handles patient check-in.
    :param patient_id: ID of the existing patient to check in.
    :param patient_data: Dictionary containing new patient details for registration.
    :return: Log message for UI display.
    """
    try:
        validate_patient_id(patient_id)

        try:
            patient = PipeLineObject.get_patient_profile(patient_id)
            clinic_state.add_to_queue(patient)
            return f"Patient retrieved and added to queue: {patient}"
        except ValueError as e:  # Patient not found
            return f"Patient not found: {e}. Please register the patient."

    except Exception as e:
        return f"Error: {e}"

def take_next_patient():
    print("\nProcessing next patient...")
    # clinic_state.current_patient = queue.pop()
    patient = clinic_state.next_in_queue()
    if not patient:
        return f"No patients in the queue."
    else:
        return patient, f"Processing Patient: {patient.fName} {patient.lName} (ID: {patient.id})"

def suggest_co_occurring_symptoms(symptoms_list):
    """Suggest co-occurring symptoms based on the current input."""
    suggested_symptoms = UseCasesAlgorithm.find_most_frequent_co_occurring_symptoms(symptoms_list)
    suggested_symptom_names = [symptom.name for symptom in suggested_symptoms]
    return suggested_symptom_names

def confirm_symptoms(symptoms_list):
    """Confirm the reported symptoms for the current patient."""
    diagnosing.reported_symptoms.extend(symptoms_list)
    return diagnosing.reported_symptoms

def suggest_diagnosed_disease():
    """Suggest potential diseases based on reported symptoms."""
    if not diagnosing.reported_symptoms:
        return []
    suggested_disease = UseCasesAlgorithm.find_most_possible_disease(diagnosing.reported_symptoms)
    suggested_disease_names = [disease["disease_name"] for disease in suggested_disease]
    return suggested_disease_names

def confirm_disease(disease):
    """Confirm and store the diagnosis for the current case."""
    if not disease:
        raise ValueError("Diagnosis cannot be empty.")
    diagnosing.diagnosed_disease = disease
    return diagnosing.diagnosed_disease

def suggest_medicines():
    if not diagnosing.reported_symptoms or not diagnosing.diagnosed_disease:
        return []
    suggested_medicines = UseCasesAlgorithm.find_relevant_medicines(
        diagnosing.reported_symptoms, diagnosing.diagnosed_disease
    )
    # Extract only the medicine names from dictionaries
    return [medicine["medicine_name"] for medicine in suggested_medicines]

def confirm_medicines(medicine_list):
    if not medicine_list:
        raise ValueError("Medicine list cannot be empty.")
    diagnosing.prescribed_medicines.extend(medicine_list)

def display_summary():
    diagnosing.diagnose_summary()

def case_complete():
    symptoms = diagnosing.reported_symptoms
    diesease = diagnosing.diagnosed_disease
    medicines = diagnosing.prescribed_medicines
    patient = clinic_state.current_patient
    UseCasesAlgorithm.patient_case_complete(patient, symptoms, diesease, medicines)
    summary = display_summary()
    # reset current diagnosing case
    diagnosing.case_reset()
    return f"Case complete:\n{patient} \n{summary}"

def create_new_patient(patient_data):
    try:
        # Extract data and validate
        validate_patient_id(patient_data["patient_id"])
        validate_patient_name(patient_data["first_name"], patient_data["last_name"])
        validate_date_of_birth(patient_data["date_of_birth"])

        # Insert into database directly
        InsertionFormula.insert_patient(patient_data)
        return f"New patient created: {patient_data['first_name']} {patient_data['last_name']} (ID: {patient_data['patient_id']})"
    except Exception as e:
        return f"Error creating patient: {e}"
    
def validate_patient_id(patient_id):
    """
    Validates the format of a patient ID.
    - Must start with a capital letter.
    - Must be followed by exactly 9 digits.
    """
    if not patient_id:
        raise ValueError("Patient ID cannot be empty.")
    if not patient_id.isalnum():
        raise ValueError("Patient ID must be alphanumeric.")
    if len(patient_id) != 10:
        raise ValueError("Patient ID must be exactly 10 characters long.")
    if not patient_id[0].isupper():
        raise ValueError("Patient ID must start with a capital letter.")
    if not patient_id[1:].isdigit():
        raise ValueError("The last 9 characters of the Patient ID must be digits.")
    
def validate_patient_name(first_name, last_name):
    """
    Validates the first and last name fields.
    :param first_name: Patient's first name.
    :param last_name: Patient's last name.
    :raises ValueError: If either field is empty.
    """
    if not first_name or not last_name:
        raise ValueError("Name fields cannot be empty.")

def validate_date_of_birth(date_of_birth):
    """
    Validates the date of birth format.
    :param date_of_birth: Patient's date of birth (YYYY-MM-DD).
    :raises ValueError: If the date format is invalid.
    """
    from datetime import datetime
    try:
        datetime.strptime(date_of_birth, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")

def get_common_symptoms():
    common_symptom_names = [symptom.name for symptom in clinic_state.recent_top_common_symptoms]
    return common_symptom_names

# some additional function:
def patient_leaves_queue(patient_id):
    for p in clinic_state.in_queue:
        if  p.id == patient_id:
            clinic_state.in_queue.remove(p)
        else:
            print(f"no patient found for id: {patient_id}")

def check_current_queue():
    
# def check_today_visits():
