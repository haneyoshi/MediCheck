# Disease Class
class Disease:
    def __init__(self,disease_name,disease_id):
        self.id = disease_id
        self.name = disease_name
    
        # object comparison
    def __eq__(self, other):
        if not isinstance(other, Disease):
            return NotImplemented
        return self.name == other.name

    def __repr__(self):
        return f"Disease(disease_id={self.id},disease_name={self.name})"