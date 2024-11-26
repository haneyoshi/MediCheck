import csv
from InsertionFormula import insert_patient

with open('RandomPatients.csv','r') as file:
            # (file name,read)
    file_reader = csv.reader(file)
    next(file_reader)
    # skip first line, it is field name

    for line in file_reader:
        # print(line)
        id = line[0]
        fName = line[1]
        lName = line [2]
        dBirth = line[3]
        patient = (id,fName,lName,dBirth)
        # print(id+","+fName+","+lName+","+dBirth)
        insert_patient(patient)