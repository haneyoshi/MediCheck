from PrescriptionUI import start_prescription_ui
import UserRequest
import tkinter as tk

def start_diagnosis_ui(app, patient):
    """Start the diagnosis entry UI."""
    diagnosis_window = tk.Toplevel(app.root)
    diagnosis_window.title("Document Diagnosis: Diagnosis")
    diagnosis_window.geometry("700x700")

    # Display patient details
    tk.Label(diagnosis_window, text="Patient Details", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(diagnosis_window, text=f"First Name: {patient.fName}").pack(pady=5)
    tk.Label(diagnosis_window, text=f"Last Name: {patient.lName}").pack(pady=5)
    tk.Label(diagnosis_window, text=f"Patient ID: {patient.id}").pack(pady=5)
    tk.Label(diagnosis_window, text=f"Date of Birth: {patient.dBirth}").pack(pady=5)

    suggested_diseases = UserRequest.suggest_diagnosed_disease()
    tk.Label(diagnosis_window, text=f"Suggested Diseases: {', '.join(suggested_diseases)}",font=("Arial", 12, "normal")).pack(pady=10)

    tk.Label(diagnosis_window, text="Enter Diagnosis:").pack()
    diagnosis_entry = tk.Entry(diagnosis_window, width=50)
    diagnosis_entry.pack(pady=5)

    def save_diagnosis():
        """Save the diagnosis and proceed to the prescription stage."""
        diagnosis = diagnosis_entry.get().strip()
        if diagnosis:
            try:
                UserRequest.confirm_disease(diagnosis)
                app.log_text.insert(tk.END, "Disease saved successfully.\n")
                diagnosis_window.destroy()
                start_prescription_ui(app, patient)
            except ValueError as ve:
                app.log_text.insert(tk.END, f"Validation Error: {ve}\n")
            except Exception as e:
                app.log_text.insert(tk.END, f"Error saving disease: {e}\n")
        else:
            app.log_text.insert(tk.END, "Error: Diagnosis cannot be empty.\n")

    tk.Button(diagnosis_window, text="Save Diagnosis", command=save_diagnosis).pack(pady=10)
