import sys
import types
import unittest
from unittest.mock import patch

# The transaction tests use fake connections and do not require the optional
# MySQL driver to be installed in the validation environment.
if "mysql.connector" not in sys.modules:
    connector_stub = types.ModuleType("mysql.connector")
    connector_stub.Error = type("DatabaseError", (Exception,), {})
    connector_stub.connect = lambda **_kwargs: None
    mysql_stub = types.ModuleType("mysql")
    mysql_stub.connector = connector_stub
    sys.modules["mysql"] = mysql_stub
    sys.modules["mysql.connector"] = connector_stub

import InsertionFormula
import UserRequest


class FakeConnection:
    def __init__(self):
        self.transactions_started = 0
        self.commits = 0
        self.rollbacks = 0
        self.closes = 0

    def start_transaction(self):
        self.transactions_started += 1

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1

    def close(self):
        self.closes += 1


class PatientStub:
    id = "A123456789"
    fName = "Test"
    lName = "Patient"


class AtomicPersistenceTests(unittest.TestCase):
    def test_complete_case_uses_one_connection_and_one_commit(self):
        connection = FakeConnection()
        calls = []

        def record(name, result):
            def operation(*args, connection=None):
                calls.append((name, args, connection))
                return result
            return operation

        with (
            patch.object(InsertionFormula, "get_connection", return_value=connection),
            patch.object(InsertionFormula, "insert_visit", side_effect=record("visit", 10)),
            patch.object(InsertionFormula, "insert_visitSymptom", side_effect=record("symptom", 1)),
            patch.object(InsertionFormula, "insert_prescription", side_effect=record("prescription", 20)),
            patch.object(InsertionFormula, "insert_prescribedMedicine", side_effect=record("medicine", 1)),
        ):
            visit_id = InsertionFormula.insert_complete_consultation(
                PatientStub.id, ["cough", "fever"], "flu", ["medicine-a", "medicine-b"]
            )

        self.assertEqual(visit_id, 10)
        self.assertEqual([call[0] for call in calls], [
            "visit", "symptom", "symptom", "prescription", "medicine", "medicine"
        ])
        self.assertTrue(all(call[2] is connection for call in calls))
        self.assertEqual(
            (connection.transactions_started, connection.commits, connection.rollbacks, connection.closes),
            (1, 1, 0, 1),
        )

    def test_middle_failure_rolls_back_without_commit(self):
        connection = FakeConnection()

        with (
            patch.object(InsertionFormula, "get_connection", return_value=connection),
            patch.object(InsertionFormula, "insert_visit", return_value=10),
            patch.object(InsertionFormula, "insert_visitSymptom", side_effect=RuntimeError("injected failure")),
        ):
            with self.assertRaisesRegex(RuntimeError, "injected failure"):
                InsertionFormula.insert_complete_consultation(
                    PatientStub.id, ["cough"], "flu", ["medicine-a"]
                )

        self.assertEqual(
            (connection.transactions_started, connection.commits, connection.rollbacks, connection.closes),
            (1, 0, 1, 1),
        )


class ConsultationStateTests(unittest.TestCase):
    def setUp(self):
        self.patient = PatientStub()
        UserRequest.clinic_state.in_queue = [self.patient]
        UserRequest.clinic_state.patients_visit_today = []
        UserRequest.begin_consultation(self.patient)

    def tearDown(self):
        UserRequest.cancel_consultation()
        UserRequest.clinic_state.in_queue = []
        UserRequest.clinic_state.patients_visit_today = []

    def test_failure_preserves_draft_and_retry_finalizes_once(self):
        symptoms = ["cough"]
        medicines = ["medicine-a"]
        with patch.object(
            UserRequest.UseCasesAlgorithm,
            "patient_case_complete",
            side_effect=[RuntimeError("database unavailable"), None],
        ) as persist:
            with self.assertRaisesRegex(RuntimeError, "database unavailable"):
                UserRequest.complete_consultation(symptoms, "flu", medicines)

            self.assertTrue(UserRequest.is_consultation_active())
            self.assertIs(UserRequest.clinic_state.current_patient, self.patient)
            self.assertEqual(UserRequest.clinic_state.in_queue, [self.patient])
            self.assertEqual(UserRequest.diagnosing.reported_symptoms, symptoms)
            self.assertEqual(UserRequest.diagnosing.diagnosed_disease, "flu")
            self.assertEqual(UserRequest.diagnosing.prescribed_medicines, medicines)

            UserRequest.complete_consultation(symptoms, "flu", medicines)

        self.assertEqual(persist.call_count, 2)
        self.assertFalse(UserRequest.is_consultation_active())
        self.assertIsNone(UserRequest.clinic_state.current_patient)
        self.assertEqual(UserRequest.clinic_state.in_queue, [])
        self.assertEqual(UserRequest.clinic_state.patients_visit_today, [self.patient])
        with self.assertRaisesRegex(ValueError, "No active consultation"):
            UserRequest.complete_consultation(symptoms, "flu", medicines)

    def test_cancel_preserves_queue_and_discards_draft(self):
        UserRequest.diagnosing.reported_symptoms = ["cough"]
        UserRequest.cancel_consultation()
        self.assertEqual(UserRequest.clinic_state.in_queue, [self.patient])
        self.assertIsNone(UserRequest.clinic_state.current_patient)
        self.assertFalse(UserRequest.is_consultation_active())
        self.assertEqual(UserRequest.diagnosing.reported_symptoms, [])


if __name__ == "__main__":
    unittest.main()
    def start_transaction(self):
        self.transactions_started += 1
