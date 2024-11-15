from ConnectDatabase import cursorExecution

# patient = (id,firstName,lastName,dateBirth)/can be a list
def insert_patient(patient):
  patientFormula = "INSERT INTO patient(patient_id, first_name, last_name, date_of_birth) VALUES (%s,%s,%s,%s)"
  cursorExecution(patientFormula,patient)

# medical_term = a string/strings
def insert_disease(medical_term):
  diseaseFormula ="INSERT INTO disease(medical_term) VALUES(%s)"
  cursorExecution(diseaseFormula,medical_term)

# name = a string/strings
def insert_medicine(name):
  medicineFormula ="INSERT INTO medicine(name) VALUES(%s)"
  cursorExecution(medicineFormula,name)

# description = a sting/strings
def insert_symptom(desciption):
  symptomFormula = "INSERT INTO symptom(description) VALUES(%s)"
  cursorExecution(symptomFormula,desciption)


def a_visit(patient_id):
  visitFormula = "INSERT INTO visit()"


