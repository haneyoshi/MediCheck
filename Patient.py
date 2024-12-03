# Patient Class
import VisitRecord
class Patient:
    def __init__(self,patient_id,first_name,last_name,date_of_birth,history = None):
        self.id = patient_id
        self.fName = first_name
        self.lName = last_name
        self.dBirth = date_of_birth
        self.records = history or []
    
    def add_visit_record(self,visit_record: VisitRecord):
        self.records.append(visit_record)
        print(f"add new visit record{visit_record} to histort: {self.records}")

        # object comparison
    def __eq__(self, other):
        if not isinstance(other, Patient):
            return NotImplemented
        return self.id == other.id

    def __repr__(self):
        return f"Patient(patient_id='{self.id}', first_name='{self.fName}',last_name='{self.lName}',date_of_birth='{self.dBirth}')"