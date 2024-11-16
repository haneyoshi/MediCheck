Create Table Patient(
patient_id VARCHAR(10),
firtst_name VARCHAR(20) NOT NULL,
last_name VARCHAR(20) NOT NULL,
date_of_birth DATE NOT NULL,
primary key(patient_id)
);

create Table Visit(
  visit_id INT AUTO_INCREMENT PRIMARY KEY,
  patient_id VARCHAR(10),
  visit_date DATETIME,
  FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
);

Create Table Symptom(
  sympton_id INT AUTO_INCREMENT PRIMARY KEY,
  sympton_name VARCHAR(50) NOT NULL,
  UNIQUE (symptom_name)
);

-- juncton table
Create Table VisitSymptom(
  visit_symptom_id INT AUTO_INCREMENT PRIMARY KEY,
  visit_id INT,
  sympton_id INT,
  FOREIGN KEY (visit_id) REFERENCES Visit(visit_id),
  FOREIGN KEY (sympton_id) REFERENCES Symptom(sympton_id)
);

create table Prescription(
  prescription_id INT AUTO_INCREMENT PRIMARY KEY,
  visit_id INT,
  disease_id INT,
  FOREIGN KEY (visit_id) REFERENCES Visit(visit_id),
  FOREIGN KEY (disease_id) REFERENCES Disease(disease_id)
);

Create Table Medicine(
  medicine_id INT AUTO_INCREMENT PRIMARY KEY,
  medicine_name VARCHAR(50) NOT NULL,
  UNIQUE (medicine_name)
);

Create Table Disease(
  disease_id INT AUTO_INCREMENT PRIMARY KEY,
  diease_name VARCHAR(50) NOT NULL,
  UNIQUE (diease_name)
);

--Junction table
Create Table PrescriptionMedicines (
  prescription_id INT,
  medicine_id INT,
  FOREIGN KEY (prescription_id) REFERENCES Prescription(prescription_id),
  FOREIGN KEY (medicine_id) REFERENCES Medicine (medicine_id)
);
