from DatabaseOperations import execute_query

def update_patient(patient_id, first_name=None, last_name=None, date_of_birth=None):
    # If no value is passed for first_name, last_name, or date_of_birth, they default to None.---> update_patient("P001", first_name="John")
    update_fields = []
    # This list collects parts of the SQL "SET" clause dynamically, based on which fields are provided
    values = []
    
    if first_name:
        # if has value
        update_fields.append("first_name = %s")
        values.append(first_name)
    if last_name:
        update_fields.append("last_name = %s")
        values.append(last_name)
    if date_of_birth:
        update_fields.append("date_of_birth = %s")
        values.append(date_of_birth)

    if not update_fields:
        raise ValueError("No fields to update")

    update_formula = f"UPDATE Patient SET {', '.join(update_fields)} WHERE patient_id = %s"
                                    # =>["fName=%s",lName=%s,dBirth=%s]
    values.append(patient_id)
    # adds the patient_id at the end of the values list to match the position of the %s placeholder in the WHERE clause.

    return execute_query(update_formula, tuple(values))
    # tuple(values) converts the list values into a tuple.MySQL requires parameters to be passed as a tuple, not a list. --> values = ["John", "Doe", "P001"] => tuple(values)  Output: ("John", "Doe", "P001")

def update_visit(visit_id, visit_date):
    if not visit_date:
        # if no value
        raise ValueError("visit_date must be provided for updating a visit")
    
    update_formula = "UPDATE Visit SET visit_date = %s WHERE visit_id = %s"
    return execute_query(update_formula, (visit_date, visit_id))

def update_symptom(symptom_id, symptom_name):
    if not symptom_name:
        raise ValueError("symptom_name must be provided for updating a symptom")
    
    update_formula = "UPDATE Symptom SET symptom_name = %s WHERE symptom_id = %s"
    return execute_query(update_formula, (symptom_name, symptom_id))

def update_medicine(medicine_id, medicine_name):
    if not medicine_name:
        raise ValueError("medicine_name must be provided for updating a medicine")
    
    update_formula = "UPDATE Medicine SET medicine_name = %s WHERE medicine_id = %s"
    return execute_query(update_formula, (medicine_name, medicine_id))

def update_disease(disease_id, disease_name):
    if not disease_name:
        raise ValueError("disease_name must be provided for updating a disease")
    
    update_formula = "UPDATE Disease SET disease_name = %s WHERE disease_id = %s"
    return execute_query(update_formula, (disease_name, disease_id))
