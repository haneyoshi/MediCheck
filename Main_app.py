import tkinter as tk
from PatientCheckInUI import patient_check_in
from PatientManagementUI import take_next_patient_ui

class MediCheckApp:
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
        self.check_in_button = tk.Button(root, text="Check In Patient", width=20, command=lambda: patient_check_in(self))
        self.check_in_button.pack(pady=5)

        # Take Next Patient Button
        self.next_patient_button = tk.Button(root, text="Take Next Patient", width=20, command=lambda: take_next_patient_ui(self))
        self.next_patient_button.pack(pady=5)

        # Exit Button
        self.exit_button = tk.Button(root, text="Exit System", width=20, command=self.exit_system)
        self.exit_button.pack(pady=5)

        # Status Label
        self.status_label = tk.Label(root, text="Welcome to MediCheck!", fg="green")
        self.status_label.pack(pady=10)

        # Status and Log Area (the widget box)
        self.log_text = tk.Text(root, height=20, width=80)
        self.log_text.pack(pady=10)

        # Display startup instructions in the log area
        self.log_text.insert(tk.END, "Here is the log:\n\n")

    def patient_check_in(self):
        """Placeholder function for Check In Patient."""
        self.log_text.insert(tk.END, "Check In button clicked.\n")

    def exit_system(self):
        """Exit the application."""
        self.root.destroy()

# for testing
if __name__ == "__main__":
    root = tk.Tk()
    app = MediCheckApp(root)
    root.mainloop()

