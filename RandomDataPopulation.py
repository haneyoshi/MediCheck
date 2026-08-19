"""Populate a newly created MediCheck database from the bundled CSV files."""

import csv

from InsertionFormula import insert_complete_consultation, insert_patient


def insert_sample_patients(csv_file="RandomPatients.csv"):
    with open(csv_file, newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            insert_patient({
                "patient_id": row["patient_id"].strip().upper(),
                "first_name": row["first_name"].strip(),
                "last_name": row["last_name"].strip(),
                "date_of_birth": row["date_of_birth"].strip(),
            })
    print("Sample patient population complete.")


def insert_sample_visits(csv_file="RandomClinicVisitData.csv"):
    with open(csv_file, newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            insert_complete_consultation(
                row["patientID"].strip().upper(),
                [item.strip() for item in row["symptoms"].split(",") if item.strip()],
                row["diagnosed_disease"].strip(),
                [item.strip() for item in row["prescribed_medicines"].split(",") if item.strip()],
                visit_date=row["visit_date"].strip(),
            )
    print("Sample visit population complete.")


def main():
    """Populate an empty schema; rerunning may encounter duplicate patient IDs."""
    insert_sample_patients()
    insert_sample_visits()
    print("MediCheck sample data population complete.")


if __name__ == "__main__":
    main()
