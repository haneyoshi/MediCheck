# Patient Class
class Patient:
    def __init__(self,patient_id,first_name,last_name,date_of_birth):
        self.id = patient_id
        self.fName = first_name
        self.lName = last_name
        self.dBirth = date_of_birth
    def getId(self):
        return self.id
    def getFName(self):
        return self.fName
    def getLName(self):
        return self.lName
    def getBDate(self):
        return self.dBirth
    def getPatientInfo(self):
        print(self.id+","+self.fName+","+self.lName+","+self.dBirth)