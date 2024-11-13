Create Table Patient(
patient_id VARCHAR(10),
firtst_name VARCHAR(20),
last_name VARCHAR(20),
date_of_birth date,
primary key(patient_id)
);

create Table Visit(
  visit_id INT AUTO_INCREMENT PRIMARY KEY,
  patient_id VARCHAR(10),
  prescription_id INT,
  FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
  FOREIGN KEY (prescription_id) REFERENCES Prescription(prescription_id)
)

Create Table Symptom(
  sympton_id INT AUTO_INCREMENT PRIMARY KEY,
  sympton VARCHAR(50)
)

-- juncton table
Create Table VisitSymptom(
  visit_id INT,
  sympton_id INT
  FOREIGN KEY (visit_id) REFERENCES Visit(visit_id),
  FOREIGN KEY (sympton_id) REFERENCES Symptom(sympton_id)
)

create table Prescription(
  prescription_id INT AUTO_INCREMENT PRIMARY KEY,
  visit_id INT
  FOREIGN KEY (visit_id) REFERENCES Visit(visit_id),
);

Create Table Medicine(
  medicine_id INT AUTO_INCREMENT PRIMARY KEY,
  medicine VARCHAR(50),
)

Create Table Disease(
  disease_id INT AUTO_INCREMENT PRIMARY KEY,
  diease VARCHAR(50)
)

--Junction table
Create Table PresMedicine(
  prescription_id INT,
  medicine_id INT,
  FOREIGN KEY (prescription_id) REFERENCES Prescription(prescription_id),
  FOREIGN KEY (medicine_id) REFERENCES Medicine (medicine_id)
)

--Junction table
Create Table PresDisease(
  prescription_id INT,
  disease_id INT,
  FOREIGN KEY (prescription_id) REFERENCES Prescription (prescription_id),
  FOREIGN KEY (disease_id) REFERENCES Disease (disease_id)
)