import tkinter as tk
from tkinter import ttk

import UserRequest
from UIUtils import create_card


class CheckInView(ttk.Frame):
    """Integrated existing-patient check-in and new-patient registration."""

    FIELDS = (
        ("patient_id", "Patient ID", "One capital letter and nine digits"),
        ("first_name", "First name", "Required"),
        ("last_name", "Last name", "Required"),
        ("date_of_birth", "Date of birth", "YYYY-MM-DD"),
    )

    def __init__(self, parent, app, initial_mode="existing"):
        super().__init__(parent, style="App.TFrame")
        self.app, self.mode = app, initial_mode
        self.values = {name: tk.StringVar() for name, _label, _hint in self.FIELDS}
        self.errors = {name: tk.StringVar() for name, _label, _hint in self.FIELDS}
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self._build()

    def _build(self):
        for child in self.winfo_children():
            child.destroy()
        header = ttk.Frame(self, style="App.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        ttk.Label(header, text="Check In / Register", style="PageTitle.TLabel").pack(anchor="w")
        ttk.Label(header, text="Find an existing patient or create a patient record before joining the queue.", style="PageSubtitle.TLabel").pack(anchor="w", pady=(4, 0))

        modes = ttk.Frame(self, style="App.TFrame")
        modes.grid(row=1, column=0, sticky="w", pady=(0, 14))
        ttk.Button(modes, text="Check In Existing Patient", style="Active.Mode.TButton" if self.mode == "existing" else "Mode.TButton", command=lambda: self.set_mode("existing")).pack(side="left")
        ttk.Button(modes, text="Register New Patient", style="Active.Mode.TButton" if self.mode == "register" else "Mode.TButton", command=lambda: self.set_mode("register")).pack(side="left", padx=(9, 0))
        self._build_existing() if self.mode == "existing" else self._build_registration()

    def set_mode(self, mode):
        if mode != self.mode:
            self.mode = mode
            self.clear_errors()
            self._build()

    def _build_existing(self):
        card = create_card(self, 22)
        card.grid(row=2, column=0, sticky="nsew")
        card.columnconfigure(0, weight=1)
        ttk.Label(card, text="Check in an existing patient", style="CardTitle.TLabel").grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Label(card, text="Enter the patient ID to add the matching patient to the waiting queue.", style="Muted.TLabel").grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 18))
        ttk.Label(card, text="Patient ID", style="Body.TLabel").grid(row=2, column=0, columnspan=2, sticky="w")
        self.existing_entry = ttk.Entry(card, textvariable=self.values["patient_id"], style="Form.TEntry", font=("Segoe UI", 11))
        self.existing_entry.grid(row=3, column=0, sticky="ew", padx=(0, 10), pady=(6, 0), ipady=6)
        self.existing_entry.bind("<Return>", lambda _event: self.submit_existing())
        ttk.Button(card, text="Check in patient", style="Primary.TButton", command=self.submit_existing).grid(row=3, column=1, sticky="e", pady=(6, 0))
        ttk.Label(card, textvariable=self.errors["patient_id"], style="FieldError.TLabel").grid(row=4, column=0, columnspan=2, sticky="w", pady=(5, 0))
        ttk.Label(card, text="The patient record is resolved before it is added to the queue.", style="Muted.TLabel").grid(row=5, column=0, columnspan=2, sticky="w", pady=(16, 0))
        self.result_host = ttk.Frame(card, style="Surface.TFrame")
        self.result_host.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(20, 0))
        self.existing_entry.focus_set()

    def submit_existing(self):
        self.clear_errors()
        patient_id = UserRequest.normalize_patient_id(self.values["patient_id"].get())
        self.values["patient_id"].set(patient_id)
        if not patient_id:
            return self._field_error("patient_id", "Patient ID is required.")
        try:
            result = UserRequest.check_in_existing_patient(patient_id)
        except ValueError as error:
            message = str(error)
            if "No patient found" in message:
                message = f"No patient was found with ID {patient_id}. Register them first if they are new."
            return self._field_error("patient_id", message)
        except Exception:
            return self._field_error("patient_id", "Patient lookup failed. Check the database connection and try again.")
        if not result["ok"]:
            return self._field_error("patient_id", result["message"], "info")
        self._render_identity(result["patient"])
        self.values["patient_id"].set("")
        self.app.notify(result["message"], "success")

    def _build_registration(self):
        card = create_card(self, 22)
        card.grid(row=2, column=0, sticky="nsew")
        card.columnconfigure(1, weight=1)
        ttk.Label(card, text="Register a new patient", style="CardTitle.TLabel").grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Label(card, text="Create the patient record, then choose whether to add them to today’s waiting queue.", style="Muted.TLabel").grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 16))
        self.registration_entries = {}
        for index, (name, label, hint) in enumerate(self.FIELDS):
            row = 2 + index
            ttk.Label(card, text=label, style="Body.TLabel").grid(row=row, column=0, sticky="nw", padx=(0, 24), pady=(8, 0))
            field = ttk.Frame(card, style="Surface.TFrame")
            field.grid(row=row, column=1, sticky="ew", pady=(8, 0))
            field.columnconfigure(0, weight=1)
            entry = ttk.Entry(field, textvariable=self.values[name], style="Form.TEntry", font=("Segoe UI", 10))
            entry.grid(row=0, column=0, sticky="ew", ipady=5)
            entry.bind("<Return>", lambda _event: self.submit_registration(True))
            self.registration_entries[name] = entry
            ttk.Label(field, text=hint, style="Muted.TLabel").grid(row=1, column=0, sticky="w", pady=(3, 0))
            ttk.Label(field, textvariable=self.errors[name], style="FieldError.TLabel").grid(row=2, column=0, sticky="w")
        actions = ttk.Frame(card, style="Surface.TFrame")
        actions.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(22, 0))
        ttk.Button(actions, text="Clear", style="Secondary.TButton", command=self.clear_registration).pack(side="left")
        ttk.Button(actions, text="Register patient", style="Secondary.TButton", command=lambda: self.submit_registration(False)).pack(side="right")
        ttk.Button(actions, text="Register and check in", style="Primary.TButton", command=lambda: self.submit_registration(True)).pack(side="right", padx=(0, 9))
        self.registration_entries["patient_id"].focus_set()

    def submit_registration(self, check_in):
        self.clear_errors()
        data = {name: variable.get().strip() for name, variable in self.values.items()}
        data["patient_id"] = UserRequest.normalize_patient_id(data["patient_id"])
        self.values["patient_id"].set(data["patient_id"])
        if not self._validate_registration(data):
            return
        try:
            result = UserRequest.register_new_patient(data, check_in=check_in)
        except Exception as error:
            message = str(error) or "Patient registration failed."
            self.errors["patient_id"].set(message)
            self.app.notify(message, "error")
            return
        self.app.notify(result["message"], "success")
        self.clear_registration(notify=False)

    def _validate_registration(self, data):
        valid = True
        validators = (
            ("patient_id", UserRequest.validate_patient_id),
            ("date_of_birth", UserRequest.validate_date_of_birth),
        )
        if not data["first_name"]:
            self.errors["first_name"].set("First name is required.")
            valid = False
        if not data["last_name"]:
            self.errors["last_name"].set("Last name is required.")
            valid = False
        for name, validator in validators:
            try:
                validator(data[name])
            except ValueError as error:
                self.errors[name].set(str(error))
                valid = False
        if not valid:
            self.app.notify("Correct the registration fields and try again.", "error")
        return valid

    def _render_identity(self, patient):
        for child in self.result_host.winfo_children():
            child.destroy()
        ttk.Separator(self.result_host).pack(fill="x", pady=(0, 14))
        ttk.Label(self.result_host, text=patient["full_name"], style="ProfileName.TLabel").pack(anchor="w")
        ttk.Label(self.result_host, text=f"{patient['patient_id']}  •  Date of birth: {patient['date_of_birth']}", style="Muted.TLabel").pack(anchor="w", pady=(4, 0))
        ttk.Label(self.result_host, text="Added to the waiting queue", style="Success.TLabel").pack(anchor="w", pady=(8, 0))

    def _field_error(self, field, message, level="error"):
        self.errors[field].set(message)
        self.app.notify(message, level)
        return False

    def clear_errors(self):
        for variable in self.errors.values():
            variable.set("")

    def clear_registration(self, notify=True):
        for variable in self.values.values():
            variable.set("")
        self.clear_errors()
        if notify:
            self.app.notify("Registration form cleared. No patient was created.", "info")
        if hasattr(self, "registration_entries"):
            self.registration_entries["patient_id"].focus_set()


def patient_check_in(app):
    """Compatibility entry point; modern shells open the integrated workspace."""
    if hasattr(app, "show_check_in"):
        app.show_check_in("existing")
        return
    patient_id = UserRequest.normalize_patient_id(app.patient_id_entry.get())
    try:
        result = UserRequest.check_in_existing_patient(patient_id)
        message = result["message"]
    except Exception as error:
        message = f"Error: {error}"
    if hasattr(app, "log_text"):
        app.log_text.insert(tk.END, message + "\n")
