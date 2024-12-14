from DatabaseOperations import execute_query
import  DeletionFormula

def delete_related_data_for_patient(patient_id):
    """
    Deletes all data related to a specific patient, ensuring referential integrity.
    This includes visits, visit symptoms, prescriptions, prescribed medicines, etc., but retains the patient record.
    """
    try:
        # Fetch all visit IDs for the patient
        visit_query = "SELECT visit_id FROM Visit WHERE patient_id = %s"
        visits = execute_query(visit_query, (patient_id,))

        if visits:
            for visit in visits:
                visit_id = visit['visit_id']

                # Fetch and delete VisitSymptom records
                visit_symptom_query = "SELECT visit_symptom_id FROM VisitSymptom WHERE visit_id = %s"
                visit_symptoms = execute_query(visit_symptom_query, (visit_id,))

                if visit_symptoms:
                    for vs in visit_symptoms:
                        DeletionFormula.delete_visitSymptom(vs['visit_symptom_id'])

                # Fetch and delete prescriptions
                prescription_query = "SELECT prescription_id FROM Prescription WHERE visit_id = %s"
                prescriptions = execute_query(prescription_query, (visit_id,))

                if prescriptions:
                    for prescription in prescriptions:
                        prescription_id = prescription['prescription_id']

                        # Fetch and delete PrescribedMedicine records
                        prescribed_medicine_query = "SELECT medicine_id FROM PrescribedMedicine WHERE prescription_id = %s"
                        prescribed_medicines = execute_query(prescribed_medicine_query, (prescription_id,))

                        if prescribed_medicines:
                            for pm in prescribed_medicines:
                                DeletionFormula.delete_prescribedMedicine(prescription_id, pm['medicine_id'])

                        # Delete the prescription itself
                        DeletionFormula.delete_prescription(prescription_id)

                # Delete the visit itself
                DeletionFormula.delete_visit(visit_id)

        print(f"Successfully deleted all visit-related records for patient_id: {patient_id}, but retained the patient record.")

    except Exception as e:
        print(f"Error during data cleanup: {e}")

def delete_related_data_for_visit(visit_id):
    """
    Deletes all data related to a specific visit, ensuring referential integrity.
    This includes visit symptoms, prescriptions, and prescribed medicines, but retains the patient record.
    """
    try:
        # Fetch and delete VisitSymptom records
        visit_symptom_query = "SELECT visit_symptom_id FROM VisitSymptom WHERE visit_id = %s"
        visit_symptoms = execute_query(visit_symptom_query, (visit_id,))

        if visit_symptoms:
            for vs in visit_symptoms:
                DeletionFormula.delete_visitSymptom(vs['visit_symptom_id'])

        # Fetch and delete prescriptions
        prescription_query = "SELECT prescription_id FROM Prescription WHERE visit_id = %s"
        prescriptions = execute_query(prescription_query, (visit_id,))

        if prescriptions:
            for prescription in prescriptions:
                prescription_id = prescription['prescription_id']

                # Fetch and delete PrescribedMedicine records
                prescribed_medicine_query = "SELECT medicine_id FROM PrescribedMedicine WHERE prescription_id = %s"
                prescribed_medicines = execute_query(prescribed_medicine_query, (prescription_id,))

                if prescribed_medicines:
                    for pm in prescribed_medicines:
                        DeletionFormula.delete_prescribedMedicine(pm['medicine_id'])

                # Delete the prescription itself
                DeletionFormula.delete_prescription(prescription_id)

        # Delete the visit itself
        DeletionFormula.delete_visit(visit_id)

        print(f"Successfully deleted all records related to visit_id: {visit_id}, but retained the patient record.")

    except Exception as e:
        print(f"Error during visit data cleanup: {e}")

# Usage examples
def main():
    # Scenario 1: Delete all data related to a random patient
    # test_patient_id = 'P001'
    # delete_related_data_for_patient(test_patient_id)

    # Scenario 2: Delete all data related to a specific visit
    test_visit_id = 308  # Replace with an actual visit ID
    delete_related_data_for_visit(test_visit_id)

if __name__ == "__main__":
    main()
