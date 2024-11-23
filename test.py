from ReadFormula import fetch_all_patients
from Patient import Patient


all_patients  = fetch_all_patients()
# print(all_patients)
# next(all_patients)
patient_list = [Patient(**patient) for patient in all_patients]
print(repr(patient_list))