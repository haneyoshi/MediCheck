import tkinter as tk
from tkinter import messagebox, ttk

import UserRequest
from ConsultationUI import ConsultationView
from PatientCheckInUI import CheckInView
from UIUtils import COLORS, StatusBanner, bind_vertical_mousewheel, configure_styles, create_card, create_empty_state


class MediCheckApp:
    """Persistent application shell for the clinic workspace."""

    def __init__(self, root):
        self.root = root
        root.title("MediCheck Clinic Workspace")
        root.geometry("1120x720")
        root.minsize(960, 640)
        configure_styles(root)
        self.current_page = "dashboard"
        self.nav_buttons = {}
        self.page_frame = None
        self.patient_id_entry = None
        # Existing consultation screens still write to this compatibility log.
        self.log_text = tk.Text(root, height=2, width=2)
        self._build_shell()
        self.show_page("dashboard")

    def _build_shell(self):
        shell = ttk.Frame(self.root, style="App.TFrame")
        shell.grid(row=0, column=0, sticky="nsew")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        shell.rowconfigure(0, weight=1)
        shell.columnconfigure(1, weight=1)

        sidebar = ttk.Frame(shell, style="Sidebar.TFrame", width=220, padding=(18, 24))
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)
        sidebar.columnconfigure(0, weight=1)
        tk.Label(sidebar, text="MediCheck", background=COLORS["navy"], foreground="white", font=("Segoe UI", 19, "bold")).grid(row=0, column=0, sticky="w", padx=8)
        tk.Label(sidebar, text="CLINIC WORKSPACE", background=COLORS["navy"], foreground="#9EB5CA", font=("Segoe UI", 8, "bold")).grid(row=1, column=0, sticky="w", padx=8, pady=(2, 28))
        for row, (key, label) in enumerate((("dashboard", "Dashboard"), ("checkin", "Check In / Register"), ("queue", "Patient Queue"), ("patients", "Patients")), start=2):
            button = ttk.Button(sidebar, text=label, style="Nav.TButton", command=lambda page=key: self.navigate(page))
            button.grid(row=row, column=0, sticky="ew", pady=3)
            self.nav_buttons[key] = button
        sidebar.rowconfigure(6, weight=1)
        ttk.Button(sidebar, text="Exit", style="Nav.TButton", command=self.exit_system).grid(row=7, column=0, sticky="sew", pady=(24, 0))

        workspace = ttk.Frame(shell, style="App.TFrame", padding=(28, 24, 28, 18))
        workspace.grid(row=0, column=1, sticky="nsew")
        workspace.rowconfigure(0, weight=1)
        workspace.columnconfigure(0, weight=1)
        self.content = ttk.Frame(workspace, style="App.TFrame")
        self.content.grid(row=0, column=0, sticky="nsew")
        self.content.rowconfigure(0, weight=1)
        self.content.columnconfigure(0, weight=1)
        self.status_banner = StatusBanner(workspace)
        self.status_banner.grid(row=1, column=0, sticky="ew", pady=(16, 0))

    def show_page(self, page_name):
        self.current_page = page_name
        for name, button in self.nav_buttons.items():
            button.configure(style="Active.Nav.TButton" if name == page_name else "Nav.TButton")
        if self.page_frame is not None:
            self.page_frame.destroy()
        builders = {
            "dashboard": self._build_dashboard,
            "checkin": self._build_check_in,
            "queue": self._build_queue,
            "patients": self._build_patients,
            "consultation": self._build_consultation,
        }
        self.page_frame = builders.get(page_name, self._build_dashboard)(self.content)
        self.page_frame.grid(row=0, column=0, sticky="nsew")

    def navigate(self, page_name):
        if self.current_page == "consultation" and page_name != "consultation" and isinstance(self.page_frame, ConsultationView):
            self.page_frame.request_cancel(destination=page_name)
            return
        self.show_page(page_name)

    def refresh_current_view(self):
        self.show_page(self.current_page)

    def _page_header(self, parent, title, subtitle):
        header = ttk.Frame(parent, style="App.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        ttk.Label(header, text=title, style="PageTitle.TLabel").pack(anchor="w")
        ttk.Label(header, text=subtitle, style="PageSubtitle.TLabel").pack(anchor="w", pady=(4, 0))

    def _build_dashboard(self, parent):
        page = ttk.Frame(parent, style="App.TFrame")
        page.columnconfigure(0, weight=3)
        page.columnconfigure(1, weight=2)
        page.rowconfigure(3, weight=1)
        self._page_header(page, "Dashboard", "Today’s clinic activity at a glance")
        snapshot = UserRequest.get_clinic_snapshot()

        metrics = ttk.Frame(page, style="App.TFrame")
        metrics.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 18))
        for column in range(3):
            metrics.columnconfigure(column, weight=1)
        current = snapshot["current_patient"]
        values = (
            ("Patients waiting", str(snapshot["queue_count"]), "Live in-memory queue"),
            ("Completed today", str(snapshot["completed_visit_count"]), "This application session"),
            ("Current patient", current["name"] if current else "None", current["patient_id"] if current else "No active consultation"),
        )
        for column, (title, value, detail) in enumerate(values):
            card = create_card(metrics, 18)
            card.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else 7, 0 if column == 2 else 7))
            ttk.Label(card, text=title, style="Muted.TLabel").pack(anchor="w")
            ttk.Label(card, text=value, style="Metric.TLabel").pack(anchor="w", pady=(6, 1))
            ttk.Label(card, text=detail, style="Muted.TLabel").pack(anchor="w")

        checkin = create_card(page)
        checkin.grid(row=2, column=0, sticky="nsew", padx=(0, 9), pady=(0, 18))
        ttk.Label(checkin, text="Patient arrival", style="CardTitle.TLabel").grid(row=0, column=0, columnspan=2, sticky="w")
        ttk.Label(checkin, text="Choose the appropriate path for the arriving patient.", style="Muted.TLabel").grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 14))
        ttk.Button(checkin, text="Check in existing", style="Primary.TButton", command=lambda: self.show_check_in("existing")).grid(row=2, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(checkin, text="Register new patient", style="Secondary.TButton", command=lambda: self.show_check_in("register")).grid(row=2, column=1, sticky="ew", padx=(5, 0))
        checkin.columnconfigure(0, weight=1)
        checkin.columnconfigure(1, weight=1)

        actions = create_card(page)
        actions.grid(row=2, column=1, sticky="nsew", padx=(9, 0), pady=(0, 18))
        ttk.Label(actions, text="Next action", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(actions, text="Begin consultation with the first patient waiting.", style="Muted.TLabel", wraplength=290).pack(anchor="w", pady=(4, 15))
        ttk.Button(actions, text="Take next patient", style="Primary.TButton", command=self.take_next_patient).pack(fill="x")
        ttk.Button(actions, text="Find patient records", style="Secondary.TButton", command=lambda: self.show_page("patients")).pack(fill="x", pady=(9, 0))

        preview = create_card(page)
        preview.grid(row=3, column=0, columnspan=2, sticky="nsew")
        preview.columnconfigure(0, weight=1)
        ttk.Label(preview, text="Waiting room", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Button(preview, text="Open queue", style="Secondary.TButton", command=lambda: self.show_page("queue")).grid(row=0, column=1, sticky="e")
        queue = snapshot["queue"][:5]
        if not queue:
            empty = create_empty_state(preview, "Waiting room is clear", "Checked-in patients will appear here in arrival order.")
            empty.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(8, 0))
        else:
            for row, patient in enumerate(queue, start=2):
                ttk.Label(preview, text=f"{patient['position']}.  {patient['name']}", style="Body.TLabel").grid(row=row, column=0, sticky="w", pady=7)
                ttk.Label(preview, text=patient["patient_id"], style="Muted.TLabel").grid(row=row, column=1, sticky="e")
        return page

    def _build_check_in(self, parent):
        return CheckInView(parent, self, getattr(self, "checkin_mode", "existing"))

    def show_check_in(self, mode="existing"):
        self.checkin_mode = mode
        self.show_page("checkin")

    def _build_queue(self, parent):
        page = ttk.Frame(parent, style="App.TFrame")
        page.columnconfigure(0, weight=1)
        page.rowconfigure(1, weight=1)
        self._page_header(page, "Patient Queue", "Manage patients waiting for consultation")
        queue = UserRequest.get_queue_snapshot()

        card = create_card(page)
        card.grid(row=1, column=0, sticky="nsew")
        card.columnconfigure(0, weight=1)
        card.rowconfigure(1, weight=1)
        toolbar = ttk.Frame(card, style="Surface.TFrame")
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        ttk.Label(toolbar, text=f"{len(queue)} waiting", style="CardTitle.TLabel").pack(side="left")
        ttk.Button(toolbar, text="Refresh", style="Secondary.TButton", command=self.refresh_current_view).pack(side="right")
        ttk.Button(toolbar, text="Take next patient", style="Primary.TButton", command=self.take_next_patient).pack(side="right", padx=(0, 9))

        if not queue:
            empty = create_empty_state(card, "No patients waiting", "Check in an existing patient or register a new patient to begin today’s queue.", "Open Check In / Register", lambda: self.show_check_in("existing"))
            empty.grid(row=1, column=0, sticky="nsew")
            return page

        columns = ("position", "name", "patient_id")
        self.queue_tree = ttk.Treeview(card, columns=columns, show="headings", selectmode="browse")
        for column, heading in (("position", "#"), ("name", "Patient name"), ("patient_id", "Patient ID")):
            self.queue_tree.heading(column, text=heading)
        self.queue_tree.column("position", width=55, minwidth=45, anchor="center", stretch=False)
        self.queue_tree.column("name", width=320, minwidth=180)
        self.queue_tree.column("patient_id", width=180, minwidth=130)
        self.queue_tree.grid(row=1, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(card, orient="vertical", command=self.queue_tree.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.queue_tree.configure(yscrollcommand=scrollbar.set)
        for patient in queue:
            self.queue_tree.insert("", "end", iid=f"queue-{patient['position']}", values=(patient["position"], patient["name"], patient["patient_id"]))
        ttk.Button(card, text="Remove selected", style="Danger.TButton", command=self.remove_selected_patient).grid(row=2, column=0, sticky="w", pady=(14, 0))
        return page

    def _build_patients(self, parent):
        page = ttk.Frame(parent, style="App.TFrame")
        page.columnconfigure(0, weight=1)
        page.rowconfigure(2, weight=1)
        self._page_header(page, "Patients", "Search patient details and review visit history")

        search_card = create_card(page, 16)
        search_card.grid(row=1, column=0, sticky="ew", pady=(0, 18))
        search_card.columnconfigure(0, weight=1)
        ttk.Label(search_card, text="Patient ID", style="CardTitle.TLabel").grid(row=0, column=0, columnspan=3, sticky="w")
        ttk.Label(search_card, text="Enter the patient’s 10-character ID.", style="Muted.TLabel").grid(row=1, column=0, columnspan=3, sticky="w", pady=(3, 10))
        self.patient_search_entry = ttk.Entry(search_card, style="Form.TEntry", font=("Segoe UI", 11))
        self.patient_search_entry.grid(row=2, column=0, sticky="ew", padx=(0, 10), ipady=6)
        self.patient_search_entry.bind("<Return>", lambda _event: self.search_patient())
        ttk.Button(search_card, text="Search patient", style="Primary.TButton", command=self.search_patient).grid(row=2, column=1, sticky="e")
        ttk.Button(search_card, text="Clear", style="Secondary.TButton", command=self.clear_patient_search).grid(row=2, column=2, sticky="e", padx=(8, 0))

        self.patient_results = ttk.Frame(page, style="App.TFrame")
        self.patient_results.grid(row=2, column=0, sticky="nsew")
        self.patient_results.columnconfigure(0, weight=1)
        self.patient_results.rowconfigure(0, weight=1)
        self._render_patient_empty("Search by patient ID to view profile and visit history.")
        self.patient_search_entry.focus_set()
        return page

    def _build_consultation(self, parent):
        patient = UserRequest.clinic_state.current_patient
        if patient is None:
            self.notify("No patient is selected for consultation.", "error")
            return self._build_dashboard(parent)
        return ConsultationView(parent, self, patient)

    def clear_patient_search(self):
        self.patient_search_entry.delete(0, tk.END)
        self._render_patient_empty("Search by patient ID to view profile and visit history.")
        self.notify("Patient search cleared.", "info")
        self.patient_search_entry.focus_set()

    def search_patient(self):
        patient_id = UserRequest.normalize_patient_id(self.patient_search_entry.get())
        self.patient_search_entry.delete(0, tk.END)
        self.patient_search_entry.insert(0, patient_id)
        if not patient_id:
            self._render_patient_empty("Enter a patient ID to begin your search.")
            self.notify("Patient ID cannot be empty.", "error")
            self.patient_search_entry.focus_set()
            return
        try:
            profile = UserRequest.get_patient_profile_data(patient_id)
        except ValueError as error:
            message = str(error)
            if "No patient found" in message:
                message = f"No patient was found with ID {patient_id}."
            self._render_patient_empty(message)
            self.notify(message, "error")
            return
        except Exception:
            message = "Patient information could not be loaded. Check the database connection and try again."
            self._render_patient_empty(message)
            self.notify(message, "error")
            return
        self.render_patient_profile(profile)
        self.notify(f"Patient profile loaded for {profile['full_name']}.", "success")

    def _clear_patient_results(self):
        for child in self.patient_results.winfo_children():
            child.destroy()

    def _render_patient_empty(self, message):
        self._clear_patient_results()
        card = create_card(self.patient_results)
        card.grid(row=0, column=0, sticky="nsew")
        empty = create_empty_state(card, "Patient profile", message)
        empty.pack(fill="both", expand=True)

    def render_patient_profile(self, profile):
        """Render structured profile data; kept separate for focused UI testing."""
        self._clear_patient_results()
        content = ttk.Frame(self.patient_results, style="App.TFrame")
        content.grid(row=0, column=0, sticky="nsew")
        content.columnconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)

        identity = create_card(content, 18)
        identity.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        identity.columnconfigure(0, weight=2)
        identity.columnconfigure(1, weight=1)
        identity.columnconfigure(2, weight=1)
        ttk.Label(identity, text=profile["full_name"], style="ProfileName.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 24))
        ttk.Label(identity, text="Patient ID", style="Muted.TLabel").grid(row=0, column=1, sticky="w")
        ttk.Label(identity, text="Date of birth", style="Muted.TLabel").grid(row=0, column=2, sticky="w")
        ttk.Label(identity, text=f"{len(profile['visits'])} previous visit{'s' if len(profile['visits']) != 1 else ''}", style="Muted.TLabel").grid(row=1, column=0, sticky="w", pady=(4, 0))
        ttk.Label(identity, text=str(profile["patient_id"]), style="FieldValue.TLabel").grid(row=1, column=1, sticky="w", pady=(4, 0))
        ttk.Label(identity, text=self._format_date(profile["date_of_birth"]), style="FieldValue.TLabel").grid(row=1, column=2, sticky="w", pady=(4, 0))

        history = create_card(content, 16)
        history.grid(row=1, column=0, sticky="nsew")
        history.columnconfigure(0, weight=1)
        history.rowconfigure(1, weight=1)
        ttk.Label(history, text="Visit history", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 12))

        if not profile["visits"]:
            ttk.Label(history, text="No previous visits are recorded for this patient.", style="Muted.TLabel").grid(row=1, column=0, sticky="nw", pady=(8, 0))
            return

        canvas = tk.Canvas(history, background=COLORS["surface"], highlightthickness=0, borderwidth=0)
        scrollbar = ttk.Scrollbar(history, orient="vertical", command=canvas.yview)
        visits_frame = ttk.Frame(canvas, style="Surface.TFrame")
        window_id = canvas.create_window((0, 0), window=visits_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        visits_frame.bind("<Configure>", lambda _event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda event: canvas.itemconfigure(window_id, width=event.width))
        bind_vertical_mousewheel(canvas, canvas)
        canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")
        visits_frame.columnconfigure(0, weight=1)

        for row, visit in enumerate(profile["visits"]):
            visit_card = ttk.Frame(visits_frame, style="Surface.TFrame", padding=(12, 10))
            visit_card.grid(row=row, column=0, sticky="ew", pady=(0, 8))
            visit_card.columnconfigure(1, weight=1)
            ttk.Separator(visit_card, orient="horizontal").grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
            ttk.Label(visit_card, text=self._format_date(visit["visit_date"], include_time=True), style="VisitTitle.TLabel").grid(row=1, column=0, sticky="nw", padx=(0, 24))
            details = ttk.Frame(visit_card, style="Surface.TFrame")
            details.grid(row=1, column=1, sticky="ew")
            details.columnconfigure(1, weight=1)
            self._visit_detail(details, 0, "Diagnosis", visit["disease"] or "Not recorded")
            self._visit_detail(details, 1, "Symptoms", self._join_names(visit["symptoms"]))
            self._visit_detail(details, 2, "Medicines", self._join_names(visit["medicines"]))

    @staticmethod
    def _visit_detail(parent, row, label, value):
        ttk.Label(parent, text=label, style="Muted.TLabel").grid(row=row, column=0, sticky="nw", padx=(0, 16), pady=2)
        ttk.Label(parent, text=value, style="Body.TLabel", wraplength=540, justify="left").grid(row=row, column=1, sticky="nw", pady=2)

    @staticmethod
    def _join_names(values):
        return ", ".join(values) if values else "None recorded"

    @staticmethod
    def _format_date(value, include_time=False):
        if hasattr(value, "strftime"):
            return value.strftime("%b %d, %Y · %I:%M %p" if include_time else "%b %d, %Y")
        return str(value)

    def take_next_patient(self):
        patient, message = UserRequest.take_next_patient()
        if patient is None:
            self.notify(message, "info")
            self.refresh_current_view()
            return
        UserRequest.begin_consultation(patient)
        self.notify(message, "success")
        self.show_page("consultation")

    def on_consultation_cancelled(self, destination="dashboard"):
        self.notify("Consultation cancelled. The patient remains in the queue.", "info")
        self.show_page(destination)

    def on_consultation_completed(self, patient):
        self.notify(f"Visit completed for {patient.fName} {patient.lName}.", "success")
        self.show_page("dashboard")

    def remove_selected_patient(self):
        selected = self.queue_tree.selection()
        if not selected:
            self.notify("Select a patient to remove from the queue.", "error")
            return
        patient_id = self.queue_tree.item(selected[0], "values")[2]
        if not messagebox.askyesno("Remove patient", f"Remove {patient_id} from the waiting queue?", parent=self.root):
            return
        message = UserRequest.patient_leaves_queue(patient_id)
        self.notify(message, "success" if message.startswith("Patient") else "error")
        self.refresh_current_view()

    def notify(self, message, level="info"):
        self.status_banner.show(message, level)
        self.log_text.insert(tk.END, f"{message}\n")

    def exit_system(self):
        self.root.destroy()

    def complete_patient_diagnose(self):
        message = UserRequest.case_complete()
        self.notify(message, "success")
        self.refresh_current_view()


if __name__ == "__main__":
    UserRequest.program_start()
    root = tk.Tk()
    app = MediCheckApp(root)
    root.mainloop()
