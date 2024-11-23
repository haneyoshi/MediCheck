# Medicine Class

class Medicine:
    def __init__(self,medicine_name,medicine_id):
        self.id = medicine_id
        self.name = medicine_name
    
    # object comparison
    def __eq__(self, other):
        if not isinstance(other, Medicine):
            return NotImplemented
        return self.name == other.name

    def __repr__(self):
        return f"Medicine(medicine_id={self.id},medicine_name={self.name})"