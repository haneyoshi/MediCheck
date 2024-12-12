import tkinter as tk
from tkinter import messagebox
import UserRequest

class MediCheckUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MediCheck System")
        self.root.geometry("700x700")

        # Title Label
        self.title_label = tk.Label(root, text="MediCheck System", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)

        # Instructions Section
        self.instruction_text = (
            "Welcome to the MediCheck System!\n\n"
            "1) Enter patient ID or type 'new' to register a new patient, then click Check In to process check-in.\n"
            "2) Click Next Patient to start taking the next patient from the queue and document diagnosis.\n"
            "3) Click Exit to leave the program.\n"
        )
        self.instructions_label = tk.Label(root, text=self.instruction_text, justify="left", wraplength=750)
        self.instructions_label.pack(pady=10)

        # Patient ID Entry
        self.patient_id_label = tk.Label(root, text="Patient ID:")
        self.patient_id_label.pack()
        self.patient_id_entry = tk.Entry(root, width=30)
        self.patient_id_entry.pack(pady=5)

        # Check In Button
        self.check_in_button = tk.Button(root, text="Check In Patient", width=20, command=self.patient_check_in)
        self.check_in_button.pack(pady=5)

        # Take Next Patient Button
        self.next_patient_button = tk.Button(root, text="Take Next Patient", width=20, command=self.take_next_patient)
        self.next_patient_button.pack(pady=5)

        # Exit Button
        self.exit_button = tk.Button(root, text="Exit System", width=20, command=self.exit_system)
        self.exit_button.pack(pady=5)

        # Status Label
        self.status_label = tk.Label(root, text="Welcome to MediCheck!", fg="green")
        self.status_label.pack(pady=10)

         # Status and Log Area/the widget box
        self.log_text = tk.Text(root, height=20, width=80)
        self.log_text.pack(pady=10)

        # Display startup instructions in the log area
        self.log_text.insert(tk.END," Here is the log:\n\n")

    def patient_check_in(self):
        """Handle patient check-in."""
        patient_id = self.patient_id_entry.get().strip()

        if not patient_id:
            self.log_text.insert(tk.END, "Error: Please enter a patient ID.\n")
            return

        if patient_id.lower() == "new":
            # Prompt for new patient details
            new_window = tk.Toplevel(self.root)
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
                patient_data = {
                    "patient_id": patient_id_entry.get().strip(),
                    "first_name": first_name_entry.get().strip(),
                    "last_name": last_name_entry.get().strip(),
                    "date_of_birth": dob_entry.get().strip()
                }
                log = UserRequest.create_new_patient(patient_data)
                self.log_text.insert(tk.END, log + "\n")
                new_window.destroy()

            tk.Button(new_window, text="Submit", command=submit_new_patient).grid(row=4, column=0, columnspan=2, pady=10)

        else:
            # Process existing patient ID
            log = UserRequest.patient_check_in(patient_id=patient_id)
            self.log_text.insert(tk.END, log + "\n")

    def take_next_patient(self):
        """Handle patient check-in."""
        patient_id = self.patient_id_entry.get().strip()

        if not patient_id:
            self.log_text.insert(tk.END, "Error: Please enter a patient ID.\n")
            return

        if patient_id.lower() == "new":
            # Prompt for new patient details
            new_window = tk.Toplevel(self.root)
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
                patient_data = {
                    "patient_id": patient_id_entry.get().strip(),
                    "first_name": first_name_entry.get().strip(),
                    "last_name": last_name_entry.get().strip(),
                    "date_of_birth": dob_entry.get().strip()
                }
                log = UserRequest.create_new_patient(patient_data)
                self.log_text.insert(tk.END, log + "\n")
                new_window.destroy()

            tk.Button(new_window, text="Submit", command=submit_new_patient).grid(row=4, column=0, columnspan=2, pady=10)

        else:
            # Process existing patient ID
            log = UserRequest.patient_check_in(patient_id=patient_id)
            self.log_text.insert(tk.END, log + "\n")

    def exit_system(self):
        if messagebox.askokcancel("Exit", "Do you really want to exit?"):
            self.root.destroy()