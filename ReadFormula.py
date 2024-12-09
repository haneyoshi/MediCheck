from DatabaseOperations import execute_query

# Fetch specific patient
def fetch_patient_by_id(patient_id):
    query = "SELECT * FROM Patient WHERE patient_id = %s"
    return execute_query(query, (patient_id,))

# Fetch all patients
def fetch_all_patients():
    query = "SELECT * FROM Patient"
    return execute_query(query)

# Fetch visits for a specific patient
def fetch_visits_by_patient_id(patient_id):
    query = "SELECT Visit.visit_id, Visit.visit_date FROM Visit WHERE patient_id = %s"
    return execute_query(query, (patient_id,))

# Fetch a specific visit
def fetch_visit_by_id(visit_id):
    query = "SELECT * FROM Visit WHERE visit_id = %s"
    return execute_query(query, (visit_id,))

# Fetch all symptoms
def fetch_all_symptoms():
    query = "SELECT * FROM Symptom"
    return execute_query(query)

# Fetch symptoms for a specific visit
def fetch_symptoms_by_visit_id(visit_id):
    query = """
        SELECT Symptom.symptom_id, Symptom.symptom_name
        FROM VisitSymptom
        INNER JOIN Symptom ON VisitSymptom.symptom_id = Symptom.symptom_id
        WHERE VisitSymptom.visit_id = %s
    """
    return execute_query(query, (visit_id,))

# Fetch all medicines
def fetch_all_medicines():
    query = "SELECT * FROM Medicine"
    return execute_query(query)

# Fetch all diseases
def fetch_all_diseases():
    query = "SELECT * FROM Disease"
    return execute_query(query)

# Fetch prescriptions for a specific visit
def fetch_prescriptions_by_visit_id(visit_id):
    query = "SELECT prescription_id FROM Prescription WHERE visit_id = %s"
    return execute_query(query, (visit_id,))

# fetch diagnosed disease fpr a specifi presciption
def fetch_disease_by_prescription_id(prescription_id):
    print(f"\nFetching disease for prescription ID: {prescription_id}")
    query = """SELECT Disease.disease_id, Disease.disease_name
        FROM Prescription
        INNER JOIN Disease ON Prescription.disease_id = Disease.disease_id
        WHERE Prescription.prescription_id = %s
        """
    return execute_query(query,(prescription_id,))

# Fetch medicines for a specific prescription
def fetch_medicines_by_prescription_id(prescription_id):
    query = """
        SELECT Medicine.medicine_id, Medicine.medicine_name
        FROM PrescribedMedicine
        INNER JOIN Medicine ON PrescribedMedicine.medicine_id = Medicine.medicine_id
        WHERE PrescribedMedicine.prescription_id = %s
    """
    return execute_query(query, (prescription_id,))

# Fetch all data for a specific patient
def fetch_all_patient_data(patient_id):
    query = """
        SELECT Patient.*, Visit.*, Prescription.*, Disease.*, 
               Medicine.medicine_name, Symptom.symptom_name
        FROM Patient
        LEFT JOIN Visit ON Patient.patient_id = Visit.patient_id
        LEFT JOIN Prescription ON Visit.visit_id = Prescription.visit_id
        LEFT JOIN Disease ON Prescription.disease_id = Disease.disease_id
        LEFT JOIN PrescribedMedicine ON Prescription.prescription_id = PrescribedMedicine.prescription_id
        LEFT JOIN Medicine ON PrescribedMedicine.medicine_id = Medicine.medicine_id
        LEFT JOIN VisitSymptom ON Visit.visit_id = VisitSymptom.visit_id
        LEFT JOIN Symptom ON VisitSymptom.symptom_id = Symptom.symptom_id
        WHERE Patient.patient_id = %s;
    """
    return execute_query(query, (patient_id,))
    # syntax "(patient_id,)" for single parameter

# Fetch most common symptoms
def fetch_most_common_symptoms(limit=10):
    query = """
        SELECT Symptom.symptom_id, Symptom.symptom_name, COUNT(*) AS frequency
        FROM VisitSymptom
        INNER JOIN Symptom ON VisitSymptom.symptom_id = Symptom.symptom_id
        GROUP BY Symptom.symptom_name
        ORDER BY frequency DESC
        LIMIT %s;
    """
    return execute_query(query, (limit,))

# Fetch most prescribed medicines
def fetch_most_prescribed_medicines(limit=10):
    query = """
        SELECT Medicine.medicine_name, COUNT(*) AS frequency
        FROM PrescribedMedicine
        INNER JOIN Medicine ON PrescribedMedicine.medicine_id = Medicine.medicine_id
        GROUP BY Medicine.medicine_name
        ORDER BY frequency DESC
        LIMIT %s;
    """
    return execute_query(query, (limit,))

def fetch_symptom_ids_by_names(symptom_names):
    if not symptom_names:
        print("No symptom names provided.")  # Debugging
        return []
    query = "SELECT symptom_id FROM Symptom WHERE symptom_name IN (%s);"
    placeholders = ', '.join(['%s'] * len(symptom_names))
    # ['%s'] * len(symptom_names):This creates a list of %s placeholders with the length equal to the number of symptom names provided.
    # ', '.join(...): Joins all the %s placeholders into a single string separated by commas, so it matches the correct format for the IN clause.
    query = query.replace('%s', placeholders)
    # Extract the symptom_id values into a list
    result = execute_query(query, tuple(symptom_names))
    return [row['symptom_id'] for row in result] if result else []
    # syntax "tuple(symptom_names)" for multiple parameters

def fetch_disease_id_by_name(disease_name):
    query = "SELECT Disease.dease_id FROM Diease WHERE patient_name = %s"
    result = execute_query(query, (disease_name,))
    if not result:
        print(f"No disease found with name: {disease_name}")  # Debugging
        return None
    return result[0]['disease_id']

def fetch_most_possible_combinations_for_given_symptoms(symptom_names):
    # Construct SQL query
    #  Common Table Expression (CTE)
    # creates SymptomCombinations as a temporary result set, then uses it in the final query.
    # Note, CTE: 1)Non-Recursive CTEs => with..., 2)Recursive CTE => WITH RECURSIVE

    # retrieve corresponding symptom ids
    print(f"\nFetch symptom id(s) for {symptom_names}")
    symptoms = fetch_symptom_ids_by_names(symptom_names)
    if not symptoms:
        print(f"No symptom IDs found for {symptom_names}.")  # Debugging
        return []
    print(f"Results under {symptom_names}: {symptoms}")
    placeholders = ', '.join(['%s'] * len(symptoms))
    # placeholders = ", ".join(map(str, symptoms))
    count_of_symptoms = len(symptoms)
    query = f"""
    WITH SymptomCombinations AS (
        -- Get individual co-occurring symptoms for each input symptom
        SELECT vs1.symptom_id AS input_symptom, vs2.symptom_id AS co_symptom_id, COUNT(*) AS frequency
        FROM VisitSymptom vs1
        INNER JOIN VisitSymptom vs2 
            ON vs1.visit_id = vs2.visit_id AND vs1.symptom_id != vs2.symptom_id
        WHERE vs1.symptom_id IN ({placeholders})  -- Input symptoms
        GROUP BY vs1.symptom_id, vs2.symptom_id

        UNION ALL

        -- Get co-occurring symptoms for all given symptoms collectively
        SELECT vs3.symptom_id AS input_symptom, vs4.symptom_id AS co_symptom_id, COUNT(*) AS frequency
        FROM VisitSymptom vs3
        INNER JOIN VisitSymptom vs4 
            ON vs3.visit_id = vs4.visit_id AND vs3.symptom_id != vs4.symptom_id
        WHERE vs3.visit_id IN (
            SELECT visit_id
            FROM VisitSymptom
            WHERE symptom_id IN ({placeholders})
            GROUP BY visit_id
            HAVING COUNT(DISTINCT symptom_id) = %s  -- Ensure all input symptoms are present
        )
        GROUP BY vs3.symptom_id, vs4.symptom_id
    )
    -- Final Aggregation
    SELECT sc.co_symptom_id, s.symptom_name, SUM(sc.frequency) AS total_frequency
    FROM SymptomCombinations sc
    INNER JOIN Symptom s
        ON sc.co_symptom_id = s.symptom_id
    GROUP BY sc.co_symptom_id, s.symptom_name
    ORDER BY total_frequency DESC;
    """

    # Combine parameters for query execution
    params = tuple(symptoms) + tuple(symptoms) + (count_of_symptoms,)
    print(f"\nExecute query to find most possible co-occurring symptoms")
    print(f"Params: {params}")  # Debugging

    # Execute query with parameters
    results = execute_query(query, params)
    print(f"\nRaw Query Results: {results}")
    if not results:
        print("No results returned from the co-occurring symptoms query.")
    return results
    # two tuple(symptoms) for base case and recursive case respectively
    # (len(symptoms),)) %d placeholder in the HAVING COUNT(DISTINCT symptom_id) = %d clause

def fetch_most_possible_disease_for_given_symptoms(symptom_names):
    # Filtering for "All Symptoms":
    # 1)Focuses on Relevant Data, 2)Data-Driven Accuracy, 3)Simplicity and Scalability, 4)Practical Relevance
    symptoms = fetch_symptom_ids_by_names(symptom_names)
    placeholders = ', '.join(['%s'] * len(symptoms))
    query = f"""
    SELECT d.disease_name, COUNT(*) AS total_frequency
    FROM (
        SELECT visit_id
        FROM VisitSymptom
        WHERE symptom_id IN ({placeholders})
        GROUP BY visit_id
        HAVING COUNT(DISTINCT symptom_id) = %s  -- All input symptoms must be present
    ) matched_visits
    INNER JOIN Prescription p ON matched_visits.visit_id = p.visit_id
    INNER JOIN Disease d ON p.disease_id = d.disease_id
    GROUP BY d.disease_name
    ORDER BY total_frequency DESC;          
    """
     # Combine symptom IDs with the count of symptoms as parameters
    params = tuple(symptoms) + (len(symptoms),)
    print(f"Executing Query:\n{query}")
    print(f"Params: {params}")

    # Execute query
    return execute_query(query, params)

def fetch_most_relevant_medicine_for_given_symptoms_and_disease(symptom_names, disease_name):
    # Fetch relevant symptom IDs based on symptom names
    symptoms = fetch_symptom_ids_by_names(symptom_names)
    disease_id = fetch_disease_id_by_name(disease_name)

    symptom_placeholders = ', '.join(['%s'] * len(symptoms))

    # Define the query combining A (medicines for symptoms) and B (medicines for diseases)
    query = f"""
    WITH SymptomMedicines AS (
        -- Medicines prescribed for given symptoms
        SELECT pm.medicine_id, m.medicine_name, COUNT(*) AS frequency
        FROM VisitSymptom vs
        INNER JOIN Prescription p ON vs.visit_id = p.visit_id
        INNER JOIN PrescribedMedicine pm ON p.prescription_id = pm.prescription_id
        INNER JOIN Medicine m ON pm.medicine_id = m.medicine_id
        WHERE vs.symptom_id IN ({symptom_placeholders})  -- Input symptoms
        GROUP BY pm.medicine_id, m.medicine_name
    ),
    DiseaseMedicines AS (
        -- Medicines prescribed for a specific disease
        SELECT pm.medicine_id, m.medicine_name, COUNT(*) AS frequency
        FROM Disease d
        INNER JOIN Prescription p ON d.disease_id = p.disease_id
        INNER JOIN PrescribedMedicine pm ON p.prescription_id = pm.prescription_id
        INNER JOIN Medicine m ON pm.medicine_id = m.medicine_id
        WHERE d.disease_id = %s
        GROUP BY pm.medicine_id, m.medicine_name
    )
    -- Combine and aggregate results
    SELECT medicine_name, SUM(frequency) AS total_frequency
    FROM (
        SELECT * FROM SymptomMedicines
        UNION ALL
        SELECT * FROM DiseaseMedicines
    ) CombinedMedicines
    GROUP BY medicine_name
    ORDER BY total_frequency DESC;
    """
    # Execute the query with the appropriate parameters
    return execute_query(query, tuple(symptoms) + (disease_id,))




