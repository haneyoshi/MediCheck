from ConnectDatabase import cursirExecution

# patient = (id,firstName,lastName,dateBirth)/can be a list
def insert_patient(patient):
  sqlFormula = "INSERT INTO patient(patient_id, first_name, last_name, date_of_birth) VALUES (%s,%s,%s,%s)"
  cursirExecution(sqlFormula,patient)
# 
  def insert_visit()