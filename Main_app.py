import tkinter as tk
from tkinter import simpledialog, messagebox
from PatientCheckInUI import patient_check_in
from PatientManagementUI import take_next_patient_ui
import UserRequest
from QueueWindowUI import show_queue_window
from VisitWindowUI import show_visits_window
from PipeLineObject import get_patient_profile  

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

        # Remove Patient Section
        self.remove_patient_label = tk.Label(root, text="Enter Patient ID to Remove:")
        self.remove_patient_label.pack()
        self.remove_patient_entry = tk.Entry(root, width=30)
        self.remove_patient_entry.pack(pady=5)
        self.remove_patient_button = tk.Button(root, text="Remove Patient", width=20, command=self.remove_patient_from_queue)
        self.remove_patient_button.pack(pady=5)

        # Take Next Patient Button
        self.next_patient_button = tk.Button(root, text="Take Next Patient", width=20, command=lambda: take_next_patient_ui(self))
        self.next_patient_button.pack(pady=5)
        
        # Check Patients in Queue Button
        self.queue_button = tk.Button(root, text="Check Patients in Queue", width=25, command=lambda: show_queue_window(self))
        self.queue_button.pack(pady=5)

        # Check Today's Visits Button
        self.visits_button = tk.Button(root, text="Check Today's Visits", width=25, command=lambda: show_visits_window(self))
        self.visits_button.pack(pady=5)

        # Retrieve Patient Profile Button
        self.retrieve_profile_button = tk.Button(root, text="Retrieve Patient Profile", width=25, command=self.retrieve_patient_profile)
        self.retrieve_profile_button.pack(pady=5)

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

    def remove_patient_from_queue(self):
        """Handle removing a patient from the queue."""
        patient_id = self.remove_patient_entry.get().strip()
        if patient_id:
            result = UserRequest.patient_leaves_queue(patient_id)
            self.log_text.insert(tk.END, f"{result}\n")
            self.remove_patient_entry.delete(0, tk.END)
        else:
            self.log_text.insert(tk.END, "Error: Patient ID cannot be empty.\n")

    def retrieve_patient_profile(self):
        """Wrapper function to retrieve and display a patient's profile."""
        patient_id = tk.simpledialog.askstring("Input", "Enter Patient ID:")
        if not patient_id:
            self.log_text.insert(tk.END, "Error: No Patient ID provided.\n")
            return
        
        try:
            # Retrieve the patient object using the get_patient_profile function
            patient = get_patient_profile(patient_id)
            self.show_patient_profile(patient)
        except ValueError as e:
            self.log_text.insert(tk.END, f"Error: {e}\n")

    def show_patient_profile(self, patient):
        """Displays the patient's profile in a pop-up window."""
        popup = tk.Toplevel(self.root)
        popup.title(f"Patient Profile: {patient.id}")
        print("Pop-up window created successfully.")
        
        # Create a text widget to display patient information
        text_widget = tk.Text(popup, wrap=tk.WORD, width=100, height=150)
        text_widget.pack(padx=10, pady=10)
        text_widget.insert(tk.END, repr(patient))
        text_widget.config(state=tk.DISABLED)

    def exit_system(self):
        """Exit the application."""
        self.root.destroy()
    
    def complete_patient_diagnose(self):
        msg = UserRequest.case_complete()
        self.log_text.insert(tk.END, f"{msg}\n")

# for testing
if __name__ == "__main__":
    root = tk.Tk()
    app = MediCheckApp(root)
    root.mainloop()