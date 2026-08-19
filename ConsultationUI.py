import tkinter as tk
from tkinter import messagebox, ttk

import UserRequest
from UIUtils import COLORS, bind_vertical_mousewheel, create_card


class ConsultationView(ttk.Frame):
    """Single-workspace consultation with local, back-safe form state."""

    STEPS = ("Symptoms", "Diagnosis", "Prescription", "Review")

    def __init__(self, parent, app, patient):
        super().__init__(parent, style="App.TFrame")
        self.app = app
        self.patient = patient
        self.step = 0
        self.symptoms = []
        self.diagnosis = ""
        self.medicines = []
        self.diagnosis_suggestions = None
        self.medicine_suggestions = None
        self.completing = False
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self._build_header()
        self._build_progress()
        self.step_host = ttk.Frame(self, style="App.TFrame")
        self.step_host.grid(row=2, column=0, sticky="nsew")
        self.step_host.columnconfigure(0, weight=1)
        self.step_host.rowconfigure(0, weight=1)
        self._render_step()

    def _build_header(self):
        header = create_card(self, 16)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        header.columnconfigure(0, weight=2)
        header.columnconfigure(1, weight=1)
        header.columnconfigure(2, weight=1)
        ttk.Label(header, text="Consultation", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(header, text="Patient ID", style="Muted.TLabel").grid(row=0, column=1, sticky="w")
        ttk.Label(header, text="Date of birth", style="Muted.TLabel").grid(row=0, column=2, sticky="w")
        ttk.Label(header, text=f"{self.patient.fName} {self.patient.lName}", style="ProfileName.TLabel").grid(row=1, column=0, sticky="w", pady=(3, 0))
        ttk.Label(header, text=str(self.patient.id), style="FieldValue.TLabel").grid(row=1, column=1, sticky="w", pady=(3, 0))
        ttk.Label(header, text=self.app._format_date(self.patient.dBirth), style="FieldValue.TLabel").grid(row=1, column=2, sticky="w", pady=(3, 0))

    def _build_progress(self):
        self.progress = ttk.Frame(self, style="App.TFrame")
        self.progress.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        for column in range(len(self.STEPS)):
            self.progress.columnconfigure(column, weight=1)

    def _refresh_progress(self):
        for child in self.progress.winfo_children():
            child.destroy()
        for index, name in enumerate(self.STEPS):
            if index < self.step:
                prefix, background, foreground = "✓", COLORS["success_bg"], COLORS["success"]
            elif index == self.step:
                prefix, background, foreground = str(index + 1), COLORS["blue"], "white"
            else:
                prefix, background, foreground = str(index + 1), "#E6ECF3", COLORS["muted"]
            tk.Label(
                self.progress, text=f"{prefix}  {name}", background=background,
                foreground=foreground, font=("Segoe UI", 9, "bold"), padx=12, pady=9,
            ).grid(row=0, column=index, sticky="ew", padx=(0 if index == 0 else 4, 0 if index == 3 else 4))

    def _render_step(self):
        self._refresh_progress()
        for child in self.step_host.winfo_children():
            child.destroy()
        builders = (self._symptoms_step, self._diagnosis_step, self._prescription_step, self._review_step)
        body = builders[self.step]()
        body.grid(row=0, column=0, sticky="nsew")

    def _step_page(self, title, subtitle):
        page = ttk.Frame(self.step_host, style="App.TFrame")
        page.columnconfigure(0, weight=1)
        page.rowconfigure(1, weight=1)
        heading = ttk.Frame(page, style="App.TFrame")
        heading.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ttk.Label(heading, text=title, style="PageTitle.TLabel").pack(anchor="w")
        ttk.Label(heading, text=subtitle, style="PageSubtitle.TLabel").pack(anchor="w", pady=(2, 0))
        return page

    def _scrolling_content(self, page):
        holder = ttk.Frame(page, style="App.TFrame")
        holder.grid(row=1, column=0, sticky="nsew")
        holder.columnconfigure(0, weight=1)
        holder.rowconfigure(0, weight=1)
        canvas = tk.Canvas(holder, background=COLORS["canvas"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(holder, orient="vertical", command=canvas.yview)
        inner = ttk.Frame(canvas, style="App.TFrame")
        window_id = canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda _event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda event: canvas.itemconfigure(window_id, width=event.width))
        bind_vertical_mousewheel(canvas, canvas)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        inner.columnconfigure(0, weight=1)
        return inner

    def _symptoms_step(self):
        page = self._step_page("Symptoms", "Record at least one symptom before continuing")
        content = self._scrolling_content(page)
        entry_card = create_card(content, 16)
        entry_card.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        entry_card.columnconfigure(0, weight=1)
        ttk.Label(entry_card, text="Add symptom", style="CardTitle.TLabel").grid(row=0, column=0, columnspan=2, sticky="w")
        self.symptom_entry = ttk.Entry(entry_card, style="Form.TEntry", font=("Segoe UI", 11))
        self.symptom_entry.grid(row=1, column=0, sticky="ew", padx=(0, 9), pady=(10, 0), ipady=5)
        self.symptom_entry.bind("<Return>", lambda _event: self.add_symptom(self.symptom_entry.get()))
        self.symptom_entry.after_idle(self.symptom_entry.focus_set)
        ttk.Button(entry_card, text="Add", style="Primary.TButton", command=lambda: self.add_symptom(self.symptom_entry.get())).grid(row=1, column=1, pady=(10, 0))

        selected = create_card(content, 16)
        selected.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        selected.columnconfigure(0, weight=1)
        ttk.Label(selected, text="Selected symptoms", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        self.symptom_list = tk.Listbox(selected, height=max(3, min(6, len(self.symptoms) + 1)), font=("Segoe UI", 10), relief="flat", selectmode="browse", highlightthickness=1, highlightbackground=COLORS["border"], selectbackground=COLORS["blue"], selectforeground="white", activestyle="none")
        self.symptom_list.grid(row=1, column=0, sticky="ew", pady=(9, 0))
        for symptom in self.symptoms:
            self.symptom_list.insert(tk.END, symptom)
        ttk.Button(selected, text="Remove selected", style="Secondary.TButton", command=self.remove_symptom).grid(row=2, column=0, sticky="w", pady=(9, 0))

        suggestions = create_card(content, 16)
        suggestions.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        suggestions.columnconfigure(0, weight=1)
        ttk.Label(suggestions, text="Common and related symptoms", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        names = list(UserRequest.get_common_symptoms())
        if self.symptoms:
            try:
                names.extend(UserRequest.suggest_co_occurring_symptoms(self.symptoms))
            except Exception:
                self.app.notify("Related symptom suggestions are unavailable right now.", "info")
        self._suggestion_buttons(suggestions, self._unique(names), self.add_symptom, row=1)
        self._navigation(content, 3, next_command=self.continue_from_symptoms, cancel=True)
        return page

    def add_symptom(self, value):
        value = value.strip()
        if not value:
            self.app.notify("Enter a symptom before adding it.", "error")
            return
        if value.casefold() in {item.casefold() for item in self.symptoms}:
            self.app.notify(f"{value} is already selected.", "info")
            return
        self.symptoms.append(value)
        self.diagnosis = ""
        self.medicines.clear()
        self.diagnosis_suggestions = None
        self.medicine_suggestions = None
        self._render_step()
        self.app.notify(f"Added symptom: {value}.", "success")

    def remove_symptom(self):
        selection = self.symptom_list.curselection()
        if not selection:
            self.app.notify("Select a symptom to remove.", "error")
            return
        self.symptoms.pop(selection[0])
        self.diagnosis = ""
        self.medicines.clear()
        self.diagnosis_suggestions = None
        self.medicine_suggestions = None
        self._render_step()

    def continue_from_symptoms(self):
        if not self.symptoms:
            self.app.notify("Add at least one symptom before continuing.", "error")
            return
        if self.diagnosis_suggestions is None:
            try:
                self.diagnosis_suggestions = UserRequest.get_diagnosis_suggestions(self.symptoms)
            except Exception:
                self.diagnosis_suggestions = []
                self.app.notify("Diagnosis suggestions are unavailable; enter a diagnosis manually.", "info")
        self.step = 1
        self._render_step()

    def _diagnosis_step(self):
        page = self._step_page("Diagnosis", "Choose a suggestion or enter a diagnosis manually")
        content = self._scrolling_content(page)
        suggested = create_card(content, 16)
        suggested.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ttk.Label(suggested, text="Suggested diagnoses", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        self._suggestion_buttons(suggested, self.diagnosis_suggestions or [], self.set_diagnosis, row=1, empty="No suggestions available. Use manual entry below.")

        confirmed = create_card(content, 16)
        confirmed.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        confirmed.columnconfigure(0, weight=1)
        ttk.Label(confirmed, text="Confirmed diagnosis", style="CardTitle.TLabel").grid(row=0, column=0, columnspan=2, sticky="w")
        self.diagnosis_entry = ttk.Entry(confirmed, style="Form.TEntry", font=("Segoe UI", 11))
        self.diagnosis_entry.grid(row=1, column=0, sticky="ew", padx=(0, 9), pady=(10, 0), ipady=5)
        self.diagnosis_entry.insert(0, self.diagnosis)
        self.diagnosis_entry.bind("<Return>", lambda _event: self.set_diagnosis(self.diagnosis_entry.get()))
        self.diagnosis_entry.after_idle(self.diagnosis_entry.focus_set)
        ttk.Button(confirmed, text="Confirm", style="Primary.TButton", command=lambda: self.set_diagnosis(self.diagnosis_entry.get())).grid(row=1, column=1, pady=(10, 0))
        ttk.Label(confirmed, text=self.diagnosis or "No diagnosis confirmed", style="FieldValue.TLabel").grid(row=2, column=0, columnspan=2, sticky="w", pady=(12, 0))
        self._navigation(content, 2, back_command=self.go_back, next_command=self.continue_from_diagnosis, cancel=True)
        return page

    def set_diagnosis(self, value):
        value = value.strip()
        if not value:
            self.app.notify("Enter or select a diagnosis.", "error")
            return
        if value.casefold() != self.diagnosis.casefold():
            self.medicines.clear()
            self.medicine_suggestions = None
        self.diagnosis = value
        self._render_step()
        self.app.notify(f"Confirmed diagnosis: {value}.", "success")

    def continue_from_diagnosis(self):
        if not self.diagnosis:
            self.app.notify("Confirm a diagnosis before continuing.", "error")
            return
        if self.medicine_suggestions is None:
            try:
                self.medicine_suggestions = UserRequest.get_medicine_suggestions(self.symptoms, self.diagnosis)
            except Exception:
                self.medicine_suggestions = []
                self.app.notify("Medicine suggestions are unavailable; add medicines manually.", "info")
        self.step = 2
        self._render_step()

    def _prescription_step(self):
        page = self._step_page("Prescription", "Select suggested medicines or add them manually")
        content = self._scrolling_content(page)
        suggested = create_card(content, 16)
        suggested.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ttk.Label(suggested, text="Suggested medicines", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        self._suggestion_buttons(suggested, self.medicine_suggestions or [], self.add_medicine, row=1, empty="No suggestions available. Use manual entry below.")

        selected = create_card(content, 16)
        selected.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        selected.columnconfigure(0, weight=1)
        ttk.Label(selected, text="Confirmed prescription", style="CardTitle.TLabel").grid(row=0, column=0, columnspan=2, sticky="w")
        self.medicine_entry = ttk.Entry(selected, style="Form.TEntry", font=("Segoe UI", 11))
        self.medicine_entry.grid(row=1, column=0, sticky="ew", padx=(0, 9), pady=(10, 0), ipady=5)
        self.medicine_entry.bind("<Return>", lambda _event: self.add_medicine(self.medicine_entry.get()))
        self.medicine_entry.after_idle(self.medicine_entry.focus_set)
        ttk.Button(selected, text="Add medicine", style="Primary.TButton", command=lambda: self.add_medicine(self.medicine_entry.get())).grid(row=1, column=1, pady=(10, 0))
        self.medicine_list = tk.Listbox(selected, height=max(3, min(6, len(self.medicines) + 1)), font=("Segoe UI", 10), relief="flat", highlightthickness=1, highlightbackground=COLORS["border"], selectbackground=COLORS["blue"], selectforeground="white", activestyle="none")
        self.medicine_list.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        for medicine in self.medicines:
            self.medicine_list.insert(tk.END, medicine)
        ttk.Button(selected, text="Remove selected", style="Secondary.TButton", command=self.remove_medicine).grid(row=3, column=0, sticky="w", pady=(9, 0))
        self._navigation(content, 2, back_command=self.go_back, next_command=self.continue_from_prescription, next_text="Review visit", cancel=True)
        return page

    def add_medicine(self, value):
        value = value.strip()
        if not value:
            self.app.notify("Enter a medicine before adding it.", "error")
            return
        if value.casefold() in {item.casefold() for item in self.medicines}:
            self.app.notify(f"{value} is already selected.", "info")
            return
        self.medicines.append(value)
        self._render_step()
        self.app.notify(f"Added medicine: {value}.", "success")

    def remove_medicine(self):
        selection = self.medicine_list.curselection()
        if not selection:
            self.app.notify("Select a medicine to remove.", "error")
            return
        self.medicines.pop(selection[0])
        self._render_step()

    def continue_from_prescription(self):
        if not self.medicines:
            self.app.notify("Add at least one medicine before review.", "error")
            return
        self.step = 3
        self._render_step()

    def _review_step(self):
        page = self._step_page("Review visit", "Confirm the case details before saving the visit")
        content = self._scrolling_content(page)
        review = create_card(content, 18)
        review.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        review.columnconfigure(1, weight=1)
        details = (
            ("Patient", f"{self.patient.fName} {self.patient.lName} ({self.patient.id})"),
            ("Symptoms", ", ".join(self.symptoms)),
            ("Diagnosis", self.diagnosis),
            ("Medicines", ", ".join(self.medicines)),
        )
        for row, (label, value) in enumerate(details):
            ttk.Label(review, text=label, style="Muted.TLabel").grid(row=row, column=0, sticky="nw", padx=(0, 24), pady=7)
            ttk.Label(review, text=value, style="FieldValue.TLabel", wraplength=650, justify="left").grid(row=row, column=1, sticky="nw", pady=7)
        self._navigation(content, 1, back_command=self.go_back, next_command=self.complete_visit, next_text="Complete visit", cancel=True)
        return page

    def go_back(self):
        if self.step > 0:
            self.step -= 1
            self._render_step()

    def complete_visit(self):
        if self.completing:
            return
        self.completing = True
        try:
            UserRequest.complete_consultation(self.symptoms, self.diagnosis, self.medicines)
        except Exception:
            self.completing = False
            self.app.notify("The visit could not be saved. Review the database connection and try again.", "error")
            return
        self.app.on_consultation_completed(self.patient)

    def request_cancel(self, destination="dashboard", require_confirmation=True):
        if require_confirmation and not messagebox.askyesno(
            "Cancel consultation", "Discard this consultation? The patient will remain in the queue.", parent=self.app.root
        ):
            return False
        UserRequest.cancel_consultation()
        self.app.on_consultation_cancelled(destination)
        return True

    def _navigation(self, parent, row, back_command=None, next_command=None, next_text="Continue", cancel=False):
        bar = ttk.Frame(parent, style="App.TFrame")
        bar.grid(row=row, column=0, sticky="ew", pady=(6, 2))
        if cancel:
            ttk.Button(bar, text="Cancel consultation", style="Danger.TButton", command=self.request_cancel).pack(side="left")
        if next_command:
            ttk.Button(bar, text=next_text, style="Primary.TButton", command=next_command).pack(side="right")
        if back_command:
            ttk.Button(bar, text="Back", style="Secondary.TButton", command=back_command).pack(side="right", padx=(0, 8))

    @staticmethod
    def _unique(values):
        seen = set()
        return [value for value in values if value and not (value.casefold() in seen or seen.add(value.casefold()))]

    @staticmethod
    def _suggestion_buttons(parent, values, command, row, empty="No suggestions available yet."):
        frame = ttk.Frame(parent, style="Surface.TFrame")
        frame.grid(row=row, column=0, sticky="ew", pady=(10, 0))
        column_count = 3
        for column in range(column_count):
            frame.columnconfigure(column, weight=1)
        if not values:
            ttk.Label(frame, text=empty, style="Muted.TLabel").grid(row=0, column=0, columnspan=4, sticky="w")
            return
        for index, value in enumerate(values):
            ttk.Button(frame, text=value, style="Suggestion.TButton", command=lambda item=value: command(item)).grid(
                row=index // column_count, column=index % column_count, sticky="ew", padx=3, pady=3
            )
