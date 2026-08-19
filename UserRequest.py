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
consultation_active = False
consultation_completing = False
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
        result = check_in_existing_patient(patient_id)
        return result["message"]

    except Exception as e:
        return f"Error: {e}"

def check_in_existing_patient(patient_id):
    """Resolve and queue an existing patient with a presentation-safe result."""
    patient_id = normalize_patient_id(patient_id)
    validate_patient_id(patient_id)
    patient = PipeLineObject.get_patient_profile(patient_id)
    patient.id = normalize_patient_id(patient.id)
    if not clinic_state.add_to_queue(patient):
        return {
            "ok": False,
            "code": "duplicate",
            "message": f"{patient.fName} {patient.lName} is already in the waiting queue.",
            "patient": patient_to_summary_data(patient),
        }
    return {
        "ok": True,
        "code": "checked_in",
        "message": f"{patient.fName} {patient.lName} was checked in successfully.",
        "patient": patient_to_summary_data(patient),
    }

def take_next_patient():
    print("\nProcessing next patient...")
    # clinic_state.current_patient = queue.pop()
    patient = clinic_state.next_in_queue()
    if not patient:
        return None, "No patients in the queue."
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
        print(f"*** no reported_symptoms stored\n")
        return []
    suggested_disease = UseCasesAlgorithm.find_most_possible_disease(diagnosing.reported_symptoms)
    suggested_disease_names = [disease["disease_name"] for disease in suggested_disease]
    return suggested_disease_names

def get_diagnosis_suggestions(symptoms_list):
    """Return diagnosis names for an explicit symptom selection."""
    if not symptoms_list:
        return []
    results = UseCasesAlgorithm.find_most_possible_disease(symptoms_list)
    return [item["disease_name"] for item in results if item.get("disease_name") != "No relevant disease found"]

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

def get_medicine_suggestions(symptoms_list, disease):
    """Return medicine names for explicit consultation selections."""
    if not symptoms_list or not disease:
        return []
    results = UseCasesAlgorithm.find_relevant_medicines(symptoms_list, disease)
    return [item["medicine_name"] for item in results or []]

def confirm_medicines(medicine_list):
    if not medicine_list:
        raise ValueError("Medicine list cannot be empty.")
    diagnosing.prescribed_medicines.extend(medicine_list)

def display_summary():
    return diagnosing.diagnose_summary()

def case_complete():
    symptoms = diagnosing.reported_symptoms
    diesease = diagnosing.diagnosed_disease
    medicines = diagnosing.prescribed_medicines
    patient = clinic_state.current_patient
    print(f"*** UserRequest, case_complete, check key elements:\nsymptoms:{symptoms}, disease: {diesease}, medicine: {medicines}, patient.id: {patient}")
    UseCasesAlgorithm.patient_case_complete(patient, symptoms, diesease, medicines)
    summary = display_summary()
    clinic_state.case_done()
    # reset current diagnosing case
    diagnosing.case_reset()
    return summary

def begin_consultation(patient):
    """Start a clean consultation for the selected queue patient."""
    global consultation_active, consultation_completing
    if patient is None:
        raise ValueError("A patient is required to begin consultation.")
    diagnosing.case_reset()
    clinic_state.set_current_patient(patient)
    consultation_active = True
    consultation_completing = False

def cancel_consultation():
    """Discard temporary case data without removing the patient from the queue."""
    global consultation_active, consultation_completing
    diagnosing.case_reset()
    clinic_state.set_current_patient(None)
    consultation_active = False
    consultation_completing = False

def complete_consultation(symptoms, disease, medicines):
    """Validate and persist the active consultation exactly once."""
    global consultation_active, consultation_completing
    if not consultation_active or clinic_state.current_patient is None:
        raise ValueError("No active consultation is available to complete.")
    if consultation_completing:
        raise ValueError("This visit is already being completed.")
    if not symptoms:
        raise ValueError("At least one symptom is required.")
    if not disease:
        raise ValueError("A diagnosis is required.")
    if not medicines:
        raise ValueError("At least one medicine is required.")

    consultation_completing = True
    diagnosing.reported_symptoms = list(symptoms)
    diagnosing.diagnosed_disease = disease
    diagnosing.prescribed_medicines = list(medicines)
    try:
        summary = case_complete()
    except Exception:
        consultation_completing = False
        raise
    consultation_active = False
    consultation_completing = False
    return summary

def is_consultation_active():
    return consultation_active

def create_new_patient(patient_data):
    try:
        patient_data = dict(patient_data)
        patient_data["patient_id"] = normalize_patient_id(patient_data.get("patient_id"))
        # Extract data and validate
        validate_patient_id(patient_data["patient_id"])
        validate_patient_name(patient_data["first_name"], patient_data["last_name"])
        validate_date_of_birth(patient_data["date_of_birth"])

        # Insert into database directly
        result = InsertionFormula.insert_patient(patient_data)
        if not result:
            raise RuntimeError("Patient registration was not saved.")
        return f"New patient created: {patient_data['first_name']} {patient_data['last_name']} (ID: {patient_data['patient_id']})"
    except Exception as e:
        return f"Error creating patient: {e}"

def register_new_patient(patient_data, check_in=False):
    """Validate and persist a patient, optionally checking them in afterward."""
    cleaned = {
        key: str(patient_data.get(key, "")).strip()
        for key in ("patient_id", "first_name", "last_name", "date_of_birth")
    }
    cleaned["patient_id"] = normalize_patient_id(cleaned["patient_id"])
    validate_patient_id(cleaned["patient_id"])
    validate_patient_name(cleaned["first_name"], cleaned["last_name"])
    validate_date_of_birth(cleaned["date_of_birth"])
    InsertionFormula.insert_patient(cleaned)

    patient = Patient(**cleaned)
    queued = False
    if check_in:
        queued = clinic_state.add_to_queue(patient)
        if not queued:
            raise RuntimeError("Patient was registered but could not be added to the queue.")
    action = "registered and checked in" if queued else "registered"
    return {
        "ok": True,
        "code": "registered_and_checked_in" if queued else "registered",
        "message": f"{patient.fName} {patient.lName} was {action} successfully.",
        "patient": patient_to_summary_data(patient),
    }

def patient_to_summary_data(patient):
    return {
        "patient_id": patient.id,
        "full_name": f"{patient.fName} {patient.lName}",
        "date_of_birth": patient.dBirth,
    }
    
def normalize_patient_id(patient_id):
    """Return the canonical representation used for patient identity."""
    return str(patient_id).strip().upper() if patient_id is not None else ""

def validate_patient_id(patient_id):
    """
    Validates the format of a patient ID.
    - Must start with a capital letter.
    - Must be followed by exactly 9 digits.
    """
    patient_id = normalize_patient_id(patient_id)
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
    return patient_id
    
def validate_patient_name(first_name, last_name):
    """
    Validates the first and last name fields.
    :param first_name: Patient's first name.
    :param last_name: Patient's last name.
    :raises ValueError: If either field is empty.
    """
    if not first_name or not first_name.strip() or not last_name or not last_name.strip():
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

def patient_leaves_queue(patient_id):
    """Remove a patient from the queue based on their ID."""
    patient_id = normalize_patient_id(patient_id)
    for p in clinic_state.in_queue[:]:  # Iterate over a copy of the list
        if normalize_patient_id(p.id) == patient_id:
            clinic_state.in_queue.remove(p)
            return f"Patient with ID {patient_id} has been removed from the queue."
    return f"No patient found for ID: {patient_id}"

def check_current_queue():
    patient_in_queue_names = [ f"{patient.fName} {patient.lName}: {patient.id}\n" for patient in clinic_state.in_queue]
    return patient_in_queue_names

def check_today_visits():
    clinic_visit_history = [ f"{patient.fName} {patient.lName}: {patient.id}\n" for patient in clinic_state.patients_visit_today]
    return clinic_visit_history

def get_queue_snapshot():
    """Return UI-friendly queue rows without exposing mutable clinic state."""
    return [
        {
            "position": position,
            "patient_id": patient.id,
            "name": f"{patient.fName} {patient.lName}",
        }
        for position, patient in enumerate(clinic_state.in_queue, start=1)
    ]

def get_clinic_snapshot():
    """Return the live in-memory state needed by the application shell."""
    current = clinic_state.current_patient
    return {
        "queue": get_queue_snapshot(),
        "queue_count": len(clinic_state.in_queue),
        "completed_visit_count": len(clinic_state.patients_visit_today),
        "current_patient": (
            {"patient_id": current.id, "name": f"{current.fName} {current.lName}"}
            if current else None
        ),
    }

def get_patient_profile(patient_id):
    """Retrieve a patient profile through the UI/backend boundary."""
    patient_id = normalize_patient_id(patient_id)
    validate_patient_id(patient_id)
    patient = PipeLineObject.get_patient_profile(patient_id)
    patient.id = normalize_patient_id(patient.id)
    return patient

def patient_to_profile_data(patient):
    """Convert a domain Patient into stable, presentation-friendly data."""
    visits = []
    for visit in sorted(patient.records, key=lambda item: item.date, reverse=True):
        disease = visit.diagnosed_disease
        visits.append({
            "visit_id": visit.visit_id,
            "visit_date": visit.date,
            "disease": disease.name if disease else "Not recorded",
            "symptoms": [symptom.name for symptom in visit.reported_symptoms],
            "medicines": [medicine.name for medicine in visit.prescribed_medicines],
        })
    return {
        "patient_id": patient.id,
        "full_name": f"{patient.fName} {patient.lName}",
        "first_name": patient.fName,
        "last_name": patient.lName,
        "date_of_birth": patient.dBirth,
        "visits": visits,
    }

def get_patient_profile_data(patient_id):
    """Retrieve and shape a patient profile for the Patients workspace."""
    return patient_to_profile_data(get_patient_profile(patient_id))
