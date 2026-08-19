# MediCheck

MediCheck is an educational clinic-workflow prototype built as a Python/Tkinter portfolio project. It demonstrates a persistent desktop application shell, database-backed patient records, data-driven clinical suggestions, and transaction-safe visit completion.

> MediCheck is not validated clinical software and must not be used for diagnosis, treatment, or real patient care.

## Workflow

The supported application provides one integrated workflow:

1. Check in an existing patient or register a new patient.
2. Review and manage the waiting queue.
3. Take the next patient into the consultation workspace.
4. Record symptoms, review data-driven symptom and diagnosis suggestions, confirm a diagnosis, and select medicines.
5. Review and complete the visit.
6. Search the patient record and review structured visit history.

Patient IDs are normalized to uppercase throughout the application. Registration can either create the record only or create it and immediately add the patient to the queue.

## Features

- Persistent `ttk` application shell with Dashboard, Check In / Register, Patient Queue, Patients, and Consultation views
- Existing-patient check-in and new-patient registration with inline validation
- Duplicate queue protection and structured queue management
- Data-driven co-occurring symptom suggestions based on recorded visits
- Diagnosis suggestions derived from the selected symptoms
- Medicine suggestions derived from symptoms and the confirmed diagnosis
- Integrated Symptoms → Diagnosis → Prescription → Review consultation flow
- Structured patient identity and chronological visit-history presentation
- Atomic consultation persistence: visit, symptoms, diagnosis/prescription, and medicines commit as one transaction or roll back together
- Retry-safe consultation state when persistence fails

## Technology

- Python 3.10+
- Tkinter/ttk from the Python standard library
- MySQL
- `mysql-connector-python`
- Standard-library `unittest` with fake database connections for focused reliability tests

## Architecture

- `Main_app2.py` — supported application entry point and persistent shell
- `PatientCheckInUI.py` and `ConsultationUI.py` — integrated workflow views
- `UIUtils.py` — shared theme, styles, cards, empty states, and scrolling helpers
- `UserRequest.py` — boundary between UI code and application/database behavior
- `ClinicState.py` — in-memory queue and current-session state
- `UseCasesAlgorithm.py` and `PipeLineObject.py` — workflow coordination and row-to-domain mapping
- `ReadFormula.py` and `InsertionFormula.py` — database query definitions
- `DatabaseOperations.py` and `ConnectDatabase.py` — database execution and environment-based connection configuration
- `CreateTable.py` and `RandomDataPopulation.py` — schema and optional sample-data setup
- `tests/` — focused consultation-transaction and registration/check-in tests
- `docs/UI_REDESIGN_PLAN.md` — redesign history, decisions, and remaining engineering debt

## Setup

### 1. Install prerequisites

Install Python 3.10 or newer and MySQL Community Server. Tkinter is normally included with standard Windows and macOS Python distributions; some Linux distributions package it separately.

Create and activate a virtual environment, then install the runtime dependency:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 2. Create the database

Create the database before running the schema script:

```sql
CREATE DATABASE MediDatabase CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Configure the connection

MediCheck reads database settings from environment variables and otherwise uses safe local defaults:

| Variable | Default |
| --- | --- |
| `MEDICHECK_DB_HOST` | `localhost` |
| `MEDICHECK_DB_PORT` | `3306` |
| `MEDICHECK_DB_USER` | `root` |
| `MEDICHECK_DB_PASSWORD` | empty |
| `MEDICHECK_DB_NAME` | `MediDatabase` |

Set values in the terminal that launches MediCheck. For PowerShell:

```powershell
$env:MEDICHECK_DB_USER = "root"
$env:MEDICHECK_DB_PASSWORD = "your-local-password"
$env:MEDICHECK_DB_NAME = "MediDatabase"
```

`.env.example` documents the available names, but the application intentionally does not load `.env` files or require a third-party configuration package. Do not commit a populated `.env` file.

### 4. Create tables

```powershell
python CreateTable.py
```

### 5. Optional sample data

The repository includes `RandomPatients.csv` and `RandomClinicVisitData.csv`. Populate a newly created, empty schema with:

```powershell
python RandomDataPopulation.py
```

The script preserves the bundled historical visit dates. It is intended for an empty database; rerunning it may encounter duplicate patient IDs.

## Run

Use the modern supported entry point:

```powershell
python Main_app2.py
```

Startup loads common symptom data before constructing the application shell.

## Tests

The focused tests stub the optional MySQL driver when necessary and do not require a live database:

```powershell
python -m unittest tests.test_atomic_consultation tests.test_patient_registration -v
```

These tests cover transaction commit/rollback behavior, failed-transaction retry, cancellation and double-completion protection, registration persistence outcomes, patient-ID normalization, existing-patient check-in, and duplicate queue handling.

Real MySQL behavior and the complete desktop workflow have also been manually exercised for the portfolio milestone, but the automated tests are intentionally focused rather than a comprehensive clinical validation suite.

## Limitations

- Educational single-process prototype; queue and completed-today counters are session-local.
- No authentication, appointments, multi-user coordination, or production security model.
- Recommendations reflect the available demonstration data and are not medical advice.
- Database migrations, packaging, and broad automated UI testing are outside the current portfolio scope.
