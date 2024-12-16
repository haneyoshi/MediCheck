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
        self.instructions_label = tk.Label(root, text=self.instruction_text, wraplength=750)
        self.instructions_label.pack(pady=10)

        BUTTON_WIDTH = 25

        # Centered Frame for Entry Box and Label
        center_frame = tk.Frame(root)
        center_frame.pack(pady=20)

        # Patient ID Label
        self.patient_id_label = tk.Label(center_frame, text="Patient ID", font=("Arial", 14))
        self.patient_id_label.pack(pady=5)

        # Single Entry Box
        self.patient_id_entry = tk.Entry(center_frame, width=40, font=("Arial", 12))
        self.patient_id_entry.pack(pady=10)

        # Buttons Frame
        buttons_frame = tk.Frame(root)
        buttons_frame.pack(pady=10)

        # Row 1: Check In and Remove Patient
        self.check_in_button = tk.Button(buttons_frame, text="Check In Patient", width=BUTTON_WIDTH, command=lambda: patient_check_in(self))
        self.check_in_button.grid(row=0, column=0, padx=10, pady=5)

        self.remove_patient_button = tk.Button(buttons_frame, text="Remove Patient", width=BUTTON_WIDTH, command=self.remove_patient_from_queue)
        self.remove_patient_button.grid(row=0, column=1, padx=10, pady=5)

        # Row 2: Check Patients in Queue and Take Next Patient
        self.queue_button = tk.Button(buttons_frame, text="Check Patients in Queue", width=BUTTON_WIDTH, command=lambda: show_queue_window(self))
        self.queue_button.grid(row=1, column=0, padx=10, pady=5)

        self.next_patient_button = tk.Button(buttons_frame, text="Take Next Patient", width=BUTTON_WIDTH, command=lambda: take_next_patient_ui(self))
        self.next_patient_button.grid(row=1, column=1, padx=10, pady=5)

        # Row 3: Check Today's Visits and Retrieve Patient Profile
        self.visits_button = tk.Button(buttons_frame, text="Check Today's Visits", width=BUTTON_WIDTH, command=lambda: show_visits_window(self))
        self.visits_button.grid(row=2, column=0, padx=10, pady=5)

        self.retrieve_profile_button = tk.Button(buttons_frame, text="Retrieve Patient Profile", width=BUTTON_WIDTH, command=self.retrieve_patient_profile)
        self.retrieve_profile_button.grid(row=2, column=1, padx=10, pady=5)

        # Row 4: Exit System
        self.exit_button = tk.Button(buttons_frame, text="Exit System", width=BUTTON_WIDTH, command=self.exit_system)
        self.exit_button.grid(row=3, column=0, columnspan=2, pady=10)

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
        patient_id = self.patient_id_entry.get().strip()
        if patient_id:
            result = UserRequest.patient_leaves_queue(patient_id)
            self.log_text.insert(tk.END, f"{result}\n")
            self.patient_id_entry.delete(0, tk.END)
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
