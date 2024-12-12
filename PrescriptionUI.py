import UserRequest
import tkinter as tk
import textwrap

def start_prescription_ui(app, patient):
    """Start the prescription entry UI."""
    prescription_window = tk.Toplevel(app.root)
    prescription_window.title("Document Diagnosis: Prescription")
    prescription_window.geometry("700x700")

     # Display patient details
    tk.Label(prescription_window, text="Processing Patient:", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(prescription_window, text=f"First Name: {patient.fName}").pack(pady=5)
    tk.Label(prescription_window, text=f"Last Name: {patient.lName}").pack(pady=5)
    tk.Label(prescription_window, text=f"Patient ID: {patient.id}").pack(pady=5)
    tk.Label(prescription_window, text=f"Date of Birth: {patient.dBirth}").pack(pady=5)

    suggested_medicines = UserRequest.suggest_medicines()
    # Define a maximum line width
    max_width = 50
    # Wrap text into lines
    wrapped_medicines = textwrap.fill(", ".join(suggested_medicines), width=max_width)
    tk.Label(prescription_window, text=f"Suggested Medicines:\n{wrapped_medicines}",font=("Arial", 12, "normal")).pack(pady=10)

    tk.Label(prescription_window, text="Enter Prescriptions:").pack()
    prescription_entry = tk.Entry(prescription_window, width=50)
    prescription_entry.pack(pady=5)

    prescription_list = tk.Listbox(prescription_window, height=10, width=50)
    prescription_list.pack(pady=10)

    user_entered_medicines = []
    def add_prescription():
        medicine = prescription_entry.get().strip()
        if medicine:
            if medicine in user_entered_medicines:
                app.log_text.insert(tk.END, f"Error: Medicine '{medicine}' is already in the list.\n")
                return
            prescription_list.insert(tk.END, medicine)
            user_entered_medicines.append(medicine)
            app.log_text.insert(tk.END, f"Medicine '{medicine}' added successfully.\n")
            prescription_entry.delete(0, tk.END)
        else:
            app.log_text.insert(tk.END, "Error: Medicines cannot be empty.\n")

    def save_prescription():
        if not user_entered_medicines:
            app.log_text.insert(tk.END, "Error: No medicines entered to save.\n")
            return
        UserRequest.confirm_medicines(user_entered_medicines)
        app.log_text.insert(tk.END, "Prescription saved successfully.\n")
        prescription_window.destroy()

    tk.Button(prescription_window, text="Add Prescription", command=add_prescription).pack(pady=5)
    tk.Button(prescription_window, text="Save Prescription", command=save_prescription).pack(pady=10)
