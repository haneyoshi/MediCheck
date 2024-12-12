from DiagnoseUI import start_diagnosis_ui
import UserRequest
import tkinter as tk
import textwrap

def start_symptom_ui(app, patient):
    """Start the symptom entry UI."""
    symptom_window = tk.Toplevel(app.root)
    symptom_window.title("Document Diagnosis: Symptoms")
    symptom_window.geometry("700x700")

     # Display patient details
    tk.Label(symptom_window, text="Processing Patient:", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(symptom_window, text=f"First Name: {patient.fName}").pack(pady=5)
    tk.Label(symptom_window, text=f"Last Name: {patient.lName}").pack(pady=5)
    tk.Label(symptom_window, text=f"Patient ID: {patient.id}").pack(pady=5)
    tk.Label(symptom_window, text=f"Date of Birth: {patient.dBirth}").pack(pady=5)

    # display most common symptoms
    common_symptoms = UserRequest.get_common_symptoms()
    # Define a maximum line width
    max_width = 55
    # Wrap text into lines
    wrapped_symptoms = textwrap.fill(", ".join(common_symptoms), width=max_width)
    tk.Label(symptom_window, text=f"Common Symptoms:\n{wrapped_symptoms}").pack(pady=10)

    tk.Label(symptom_window, text="Enter Symptoms:").pack()
    symptom_entry = tk.Entry(symptom_window, width=50)
    symptom_entry.pack(pady=5)

    symptom_list = tk.Listbox(symptom_window, height=10, width=50)
    symptom_list.pack(pady=10)

    # Create a label for suggested symptoms
    suggestion_label = tk.Label(symptom_window, text="Suggested Symptoms: None", wraplength=600, justify="left")
    suggestion_label.pack(pady=5)

    user_entered_symptoms = []
    def add_symptom():
        symptom = symptom_entry.get().strip()
        if symptom:
            try:
                symptom_list.insert(tk.END, symptom)
                user_entered_symptoms.append(symptom)
                suggested_symptoms = UserRequest.suggest_co_occurring_symptoms(user_entered_symptoms)
                # Wrap suggestions for better readability
                wrapped_suggestions = textwrap.fill(f"Suggested Symptoms: {', '.join(suggested_symptoms)}", width=60)
                suggestion_label.config(text=wrapped_suggestions)
                symptom_entry.delete(0, tk.END)
            except Exception as e:
                app.log_text.insert(tk.END, f"Error saving Symptoms: {e}\n")
        else:
            app.log_text.insert(tk.END, "Error: Symptoms cannot be empty.\n")

    def save_symptoms():
        UserRequest.confirm_symptoms(user_entered_symptoms)
        app.log_text.insert(tk.END, "Symptoms saved successfully.\n")
        symptom_window.destroy()
        start_diagnosis_ui(app, patient)

    tk.Button(symptom_window, text="Add Symptom", command=add_symptom).pack(pady=5)
    tk.Button(symptom_window, text="Save Symptoms", command=save_symptoms).pack(pady=10)
