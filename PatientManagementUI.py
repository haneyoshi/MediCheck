from SymptomUI import start_symptom_ui
import UserRequest
import tkinter as tk

import tkinter as tk
import UserRequest

def take_next_patient_ui(app):
    """Handle the 'Take Next Patient' workflow."""
    patient, message = UserRequest.take_next_patient()

    if not patient:
        # Log message if no patient is in the queue
        app.log_text.insert(tk.END, message + "\n")
        return

    # Create a new window to display patient details
    next_patient_window = tk.Toplevel(app.root)
    next_patient_window.title("Next Patient")
    next_patient_window.geometry("500x400")

    # Display patient details
    tk.Label(next_patient_window, text="Patient Details", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(next_patient_window, text=f"First Name: {patient.fName}").pack(pady=5)
    tk.Label(next_patient_window, text=f"Last Name: {patient.lName}").pack(pady=5)
    tk.Label(next_patient_window, text=f"Patient ID: {patient.id}").pack(pady=5)
    tk.Label(next_patient_window, text=f"Date of Birth: {patient.dBirth}").pack(pady=5)

    # Next Button to proceed with symptoms entry
    def proceed_to_symptoms():
        next_patient_window.destroy()
        from SymptomUI import start_symptom_ui
        start_symptom_ui(app, patient)

    tk.Button(next_patient_window, text="Proceed to Symptoms", command=proceed_to_symptoms).pack(pady=10)
   
