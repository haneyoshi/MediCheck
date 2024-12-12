import tkinter as tk
import UserRequest

def patient_check_in(app):
    """Handle patient check-in."""
    patient_id = app.patient_id_entry.get().strip()

    if not patient_id:
        app.log_text.insert(tk.END, "Error: Please enter a patient ID.\n")
        return

    if patient_id.lower() == "new":
        # Open a new window for registering a new patient
        new_window = tk.Toplevel(app.root)
        new_window.title("Register New Patient")

        tk.Label(new_window, text="Patient ID:").grid(row=0, column=0, padx=10, pady=5)
        patient_id_entry = tk.Entry(new_window)
        patient_id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(new_window, text="First Name:").grid(row=1, column=0, padx=10, pady=5)
        first_name_entry = tk.Entry(new_window)
        first_name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(new_window, text="Last Name:").grid(row=2, column=0, padx=10, pady=5)
        last_name_entry = tk.Entry(new_window)
        last_name_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(new_window, text="Date of Birth (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5)
        dob_entry = tk.Entry(new_window)
        dob_entry.grid(row=3, column=1, padx=10, pady=5)

        def submit_new_patient():
            """Submit new patient details to the backend."""
            patient_data = {
                "patient_id": patient_id_entry.get().strip(),
                "first_name": first_name_entry.get().strip(),
                "last_name": last_name_entry.get().strip(),
                "date_of_birth": dob_entry.get().strip(),
            }

            # Call backend to register the patient
            log = UserRequest.create_new_patient(patient_data)
            app.log_text.insert(tk.END, log + "\n")

            if "Error" not in log:
                # Clear the patient ID entry after successful registration
                app.patient_id_entry.delete(0, tk.END)

            new_window.destroy()

        # Submit button in the new patient window
        tk.Button(new_window, text="Submit", command=submit_new_patient).grid(row=4, column=0, columnspan=2, pady=10)

    else:
        # Process existing patient ID
        log = UserRequest.patient_check_in(patient_id=patient_id)
        app.log_text.insert(tk.END, log + "\n")

        if "Error" not in log:
            # Clear the patient ID entry after successful check-in
            app.patient_id_entry.delete(0, tk.END)
