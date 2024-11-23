

all_patients = fetch_all_patients()
patient_objects = [Patient(**patient) for patient in all_patients]
print(patient_objects)