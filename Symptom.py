# Symptom Class

class Symptom:
    def __init__(self,symptom_name,symptom_id):
        self.id = symptom_id
        self.name = symptom_name
    
        # object comparison
    def __eq__(self, other):
        if not isinstance(other, Symptom):
            return NotImplemented
        return self.name == other.name
    
    def __repr__(self):
        return f"Symptom(symptom_id={self.id},symptom_name={self.name})"