import UpdateFormula
import pandas as pd
from DatabaseOperations import execute_query

# Load CSV data
csv_file = 'RandomClinicVisitData.csv'
df = pd.read_csv(csv_file)

# Query to fetch visit IDs
visits_query = "SELECT visit_id FROM Visit ORDER BY visit_id ASC"
visit_id_list = execute_query(visits_query)

# Extract visit_id values from the result
visit_ids = [record['visit_id'] for record in visit_id_list]

# Ensure the number of IDs matches the CSV rows
if len(visit_ids) < len(df):
    raise ValueError("Not enough visit IDs in the database to update all records from the CSV file.")

# Iterate through the DataFrame and update visit dates
id_count = 0
for _, row in df.iterrows():
    visit_date = row['visit_date']
    visit_id = visit_ids[id_count]  # Get the corresponding visit_id
    try:
        UpdateFormula.update_visit(visit_id, visit_date)  # Update visit
    except Exception as e:
        print(f"Error updating visit_id {visit_id}: {e}")
    id_count += 1  # Increment the counter