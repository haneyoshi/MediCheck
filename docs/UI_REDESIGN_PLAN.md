# MediCheck UI Redesign Working Plan

## Pre-redesign baseline

The original launcher initialized database-backed startup state through `UserRequest.program_start()` and created the root application from `Main_app2.py`. The original root screen was a command-style dashboard with one patient-ID entry, action buttons, a status label, and a shared text log. The supported entry point is now `Main_app2.py`, which performs its own startup initialization.

The UI is split across function-based modules. Check-in/registration, queue, visits, patient selection, symptoms, diagnosis, prescriptions, and summary each create widgets directly, usually in a new `Toplevel`. `UIUtils.py` currently contains only basic grid label/button helpers.

`UserRequest.py` is the intended application boundary. It owns process-global `ClinicState` and `Diagnosing` instances, validates input, coordinates use cases, and returns a mixture of strings, domain objects, tuples, and lists. Behind it, `UseCasesAlgorithm.py` coordinates persistence and recommendations; `PipeLineObject.py` maps database rows into domain objects; `ReadFormula.py` and `InsertionFormula.py` define SQL operations; and `DatabaseOperations.py` opens a new MySQL connection for each query. `CreateTable.py` defines the schema.

## Current user workflow

1. Startup loads common symptoms from visit history and opens the main window.
2. Staff open the integrated Check In / Register workspace and choose an explicit existing-patient or new-patient path. Registration can intentionally save only or save and add the patient to the waiting queue.
3. Staff can inspect or remove queued patients, view visits completed during this process, or retrieve a database-backed patient profile.
4. **Take Next Patient** selects the first queued patient and opens patient details.
5. Consultation advances through separate Symptoms → Diagnosis → Prescription → Summary windows. Suggestions are derived from historical database records.
6. Opening the summary persists the visit, symptoms, diagnosis, and medicines, removes the patient from the queue, records the visit in today's in-memory list, and resets consultation state.

## Major UI/UX weaknesses

- The main screen is a fixed-size collection of equally weighted buttons and instructions rather than a task-focused clinic dashboard; resizing and responsive layout are not configured.
- Normal work launches a long chain of independent `Toplevel` windows. There is no persistent navigation, visible step state, back/cancel recovery, or protection against starting overlapping consultations.
- Styling and widget construction are duplicated across modules; native `tk` widgets, hard-coded Arial fonts, dimensions, spacing, and colors provide little hierarchy or consistency.
- Queue and visit screens flatten records into strings inside read-only `Text` widgets. Patient history displays `repr(patient)`, exposing implementation formatting instead of scannable structured data.
- Feedback is split between a large append-only log, modal windows, and console `print` calls. Errors often appear in the obscured root log rather than beside the active control.
- Forms lack field-level validation feedback, required-field cues, sensible focus/keyboard behavior, duplicate-removal controls for entered items, and confirmation of consequential actions.
- Suggestions are passive comma-separated text; they cannot be selected directly and do not communicate empty/loading/error states.
- Check-in and registration are now integrated into the shell with explicit modes, inline validation, and truthful persistence feedback.
- Queue and today's-visits views are snapshots with no refresh, useful metadata, selection, or contextual actions.

## Reusable UI opportunities

- A single `ttk` application shell with header/navigation, a content region, persistent status/notification area, and view switching.
- Central theme tokens for fonts, spacing, colors, widget styles, and window sizing in an expanded UI utility/theme module.
- Reusable page header, patient identity banner, labeled form field, validation message, empty/error/loading state, action bar, and confirmation dialog.
- `ttk.Treeview`-based patient, queue, and visit tables with consistent selection and refresh behavior.
- Structured patient profile and visit-history components, including visit detail sections for symptoms, diagnosis, and medicines.
- One consultation workspace/stepper that retains patient context while swapping Symptoms, Diagnosis, Prescription, and Review panels.
- Selectable suggestion chips/list rows and reusable editable-list controls for symptoms and medicines.
- Stable result types from `UserRequest.py` so views do not infer success by searching returned strings for `"Error"`.

## Backend defects and technical debt affecting redesign

These are findings to plan around, not fixes included in this documentation task.

- `ClinicState.next_in_queue()` indexes `in_queue[0]` before checking emptiness, while `UserRequest.take_next_patient()` expects a falsy result. Taking a patient from an empty queue therefore raises `IndexError`; its return shape is also inconsistent (string versus `(patient, message)`).
- `InsertionFormula.insert_visit()` executes the same INSERT twice and returns the second ID, creating duplicate visits and associating the consultation data only with one of them.
- `DatabaseOperations.get_or_insert()` constructs `{column}_id`/`{column}_name` conventions that do not work for `Patient`. `create_new_patient()` does not check a failed/`None` insert, so it can report success after a database failure.
- `ReadFormula.fetch_disease_id_by_name()` contains misspelled table/column names (`Diease`, `dease_id`, `patient_name`), blocking disease-based medicine recommendations. The medicine query may subsequently receive a null disease ID.
- `ReadFormula.fetch_most_possible_disease_for_given_symptoms()` binds parameters in an order that does not match its SQL (the divisor placeholder appears before symptom placeholders). Empty/unrecognized symptom input can also produce invalid/unsafe query semantics.
- `ReadFormula.fetch_disease_by_id()` returns database rows, but `PipeLineObject.py` passes that list directly as a `Disease` name. Patient history can therefore contain malformed disease display data.
- Consultation completion now persists the Visit, symptom links, Prescription/diagnosis, and medicine links through one shared transaction. Failures roll back and propagate to the consultation workflow so its draft and queue state remain retryable.
- Consultation and queue state are process-global and mutable. Duplicate check-ins are allowed; selecting the next patient does not reserve/pop them; canceling a consultation does not reset accumulated diagnosis state; and multiple consultation windows can corrupt shared state.
- Patient profile retrieval previously bypassed the preferred boundary; the modern Patients workspace now uses `UserRequest.py`.
- Repository-readiness cleanup moved database configuration to environment variables, made `CreateTable.py` safe to import, and aligned README setup with `MediDatabase`.
- Patient IDs now use the schema-compatible 10-character format and are normalized to uppercase before validation and persistence.
- Queue and today's visits exist only in memory, so UI labels should not imply cross-session or multi-user persistence.

## Proposed UI architecture

Keep `Main.py` as the composition entry point and evolve `MediCheckApp` into a single root shell. The shell should own navigation and swap reusable `ttk.Frame` views: Dashboard, Queue, Patients, Consultation, and optionally Settings/About. Reserve `Toplevel` for genuinely modal confirmations or short focused dialogs.

Views should call only `UserRequest.py`. Evolve that boundary incrementally toward predictable structured responses/view models (patient summary, queue row, visit summary, action result) without replacing the domain/database layers wholesale. The shell should own selected-patient and active-view state; backend consultation state should have explicit start, cancel, and complete lifecycle operations. Components and theme definitions should live in clearly named shared UI modules rather than accumulating screen-specific helpers.

## Implementation phases

### Phase 1 — UI foundation and app shell

- Establish `ttk` theme tokens, reusable components, root resizing/minimum size, content navigation, and a consistent notification/error pattern.
- Introduce view switching in the root window while preserving existing commands and the `UserRequest.py` boundary.
- Define structured UI-facing result shapes needed by the dashboard/queue; fix only reliability blockers necessary to render and exercise the shell.

### Phase 2 — Dashboard and queue

- Build a focused dashboard with queue count, current/next patient context, primary check-in and take-next actions, and today's completed-visit count.
- Replace queue text with a refreshable structured table and contextual remove/select actions.
- Prevent duplicate queue entries, handle an empty queue safely, and make active-consultation state visible.

### Phase 3 — Patient search, profile, and history

- Replace the prompt-plus-`repr` profile flow with in-page search, a patient identity/details panel, and structured chronological visit history.
- Route profile retrieval through `UserRequest.py` and normalize malformed disease/history data.
- Provide clear not-found, database-error, and no-history states.

### Phase 4 — Consultation workflow

- Consolidate patient details, symptoms, diagnosis, prescription, and review into one step-based workspace.
- Make suggestions selectable, allow removal/editing, validate each step locally, and support explicit cancel/recovery without leaking state.
- Make final persistence atomic and show success only after the complete case is saved; correct duplicate visit insertion and recommendation-query defects as part of this milestone.

### Phase 5 — Check-in and registration refinement

- Replace the `new` sentinel with explicit existing-patient and new-patient paths. **Completed in Phase 5.**
- Add inline validation, focus/keyboard flow, clear success/error states, and an intentional register-and-check-in option.
- Make persistence outcomes trustworthy and centralize database configuration.

### Phase 6 — Backend reliability cleanup and final polish

- Finish stable `UserRequest` contracts, transaction/error handling, state lifecycle safeguards, and documentation/configuration alignment that were not prerequisites earlier.
- Improve accessibility, empty/loading states, copy, spacing, responsive behavior, and keyboard navigation.
- Perform focused end-to-end validation of the preserved clinic workflow and capture updated portfolio screenshots/documentation.

## Current implementation status and next milestone

The persistent shell, Dashboard, structured Queue, integrated Patients workspace, and integrated Consultation workspace are now implemented. Consultation uses a dedicated `ConsultationView` with local draft selections, persistent patient context, step navigation, and an explicit `UserRequest.py` begin/cancel/complete lifecycle. Local draft state prevents Back navigation from duplicating global diagnosis data; only the final Complete action copies the selections to the backend case and persists them.

Phase 4 corrected duplicate Visit insertion, disease-recommendation parameter order, disease-name lookup for medicine suggestions, and stale consultation state across start/cancel/complete. Normal UI completion is guarded against double submission. Phase 4.5 makes the complete-case write sequence atomic: it commits once only after the Visit, symptom links, Prescription/diagnosis, and medicine links all succeed, or rolls back while preserving the active consultation draft for retry.

Phase 5 integrates check-in and registration into the persistent shell. The normal workflow now exposes explicit **Check In Existing Patient** and **Register New Patient** modes instead of the `new` sentinel or a registration `Toplevel`. Registration uses the existing patient ID, first name, last name, and date-of-birth schema with inline validation and explicit **Register patient** versus **Register and check in** actions. Database failures propagate through `UserRequest` and no longer produce false success or queue nonexistent patients. Existing-patient check-in resolves a presentation-safe identity summary and prevents duplicate queue entries.

Remaining check-in/registration debt is limited to real-MySQL integration verification and the broader database-configuration cleanup already deferred from this milestone. The next milestone is Phase 6: final cross-application UI polish, portfolio-readiness review, and focused remaining reliability defects that materially affect the demonstrated workflow.

### Phase 6 portfolio polish

Phase 6 completed a focused consistency pass across the modern shell. Shared styles now cover form inputs, mode selectors, suggestion actions, destructive actions, and intentional empty states. Dashboard, Queue, Patients, Check In / Register, and Consultation use the same action hierarchy and surface treatment; consultation entry focus and scroll-wheel behavior were improved, suggestion controls are visually distinct from confirmed selections, and queue removal/cancellation are consistently identified as destructive actions. The minimum shell size was adjusted to protect the demonstrated layouts without making the application fixed-size.

The modern Dashboard no longer exposes the legacy raw-text Today’s Visits popup. Completed-session count remains visible on the Dashboard, while structured patient records remain available through Patients. Legacy popup modules are retained only for compatibility with older launchers.

Portfolio-demo/core-workflow status: no known code-level presentation blocker remains in the modern shell, and focused mocked tests cover consultation transactions plus registration/check-in state behavior. Interactive visual inspection is still required at the minimum, default, and larger window sizes, including long suggestions and visit histories. Real MySQL registration, lookup, recommendations, consultation persistence, and history refresh have not been validated in this environment.

Repository-readiness cleanup centralized database configuration, removed embedded credentials and generated artifacts, aligned setup documentation, and retired the verified-unused popup UI chain. Longer-term engineering improvements remain deferred: database migrations, packaging, stable result contracts for maintenance APIs, and removal of remaining console diagnostics. The recommended next step is the deliberate portfolio milestone commit.
