from RecordInsertion import cursorInsertion
# this module specify data-insertion instruction for each table 

# patient = (id,firstName,lastName,dateBirth)/can be a list
def insert_patient(patient):
  patientFormula = "INSERT INTO Patient(patient_id, first_name, last_name, date_of_birth) VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE patient_id = LAST_INSERT_ID (patient_id)"
# ON DUPLICATE KEY:This clause handles the case where a duplicate symptom_name is detected (based on the UNIQUE constraint). Instead of throwing an error, the database executes the UPDATE part.
# The LAST_INSERT_ID() function is typically used to retrieve the auto-incremented ID of the last inserted row. By passing symptom_id to LAST_INSERT_ID() in the UPDATE statement, MySQL ensures that: If the row is inserted (a new record), LAST_INSERT_ID() returns the new auto-incremented symptom_id. If the row is updated (a duplicate is found), LAST_INSERT_ID() returns the existing symptom_id of the updated row.
  # return_patient_id
  return cursorInsertion(patientFormula, patient)

# disease_name = a string/strings
def insert_disease(disease_name):
  diseaseFormula ="INSERT INTO Disease(disease_name) VALUES(%s) ON DUPLICATE KEY UPDATE disease_id = LAST_INSERT_ID(disease_id)"
  #return_disease_id
  return cursorInsertion(diseaseFormula,disease_name)

# medicine_name = a string/strings
def insert_medicine(medicine_name):
  medicineFormula ="INSERT INTO Medicine(medicine_name) VALUES(%s) ON DUPLICATE KEY UPDATE medicine_id = LAST_INSERT_ID(medicine_id)"
  #return_medicine_id
  return cursorInsertion(medicineFormula,medicine_name)

# symptom_name = a sting/strings
def insert_symptom(symptom_name):
  symptomFormula = "INSERT INTO Symptom(symptom_name) VALUES(%s) ON DUPLICATE KEY UPDATE symptom_id = LAST_INSERTID(symptom_id)"
  # return_symptom_id
  return cursorInsertion(symptomFormula,symptom_name)


def insert_visit(patient_id):
  visitFormula = "INSERT INTO Visit(patient_id) VALUES(%s)"
  # return_vise_id
  return cursorInsertion(visitFormula,patient_id)

def insert_prescription(visit_id,disease_name):
  disease_id  = insert_disease(disease_name)
  prescriptionFormula = "INSERT INTO Prescription(visit_id,disease_id) VALUES(%s,%s)"
  return cursorInsertion(prescriptionFormula,visit_id,disease_id)

def insert_visitSymptom(visit_id,symptom_name):
  symptom_id = insert_symptom(symptom_name)
  visitSymptomFormula = "INSERT INTO VistiSymptom(visit_id,symptom_name) VALUES(%s,%s)"
  return cursorInsertion(visitSymptomFormula, visit_id, symptom_id)

def insert_prescribedMedicine(prescription_id,medicine_name):
  medicine_id = insert_medicine(medicine_name)
  prescribedMedicineFormula = "INSERT INTO PrescribedMedicine(precription_id,medicine_id) VALUES (%s,%s)"
  return cursorInsertion(prescribedMedicineFormula,prescription_id,medicine_id)