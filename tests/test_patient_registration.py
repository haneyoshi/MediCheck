import sys
import types
import unittest
from unittest.mock import patch

if "mysql.connector" not in sys.modules:
    connector_stub = types.ModuleType("mysql.connector")
    connector_stub.Error = type("DatabaseError", (Exception,), {})
    connector_stub.connect = lambda **_kwargs: None
    mysql_stub = types.ModuleType("mysql")
    mysql_stub.connector = connector_stub
    sys.modules["mysql"] = mysql_stub
    sys.modules["mysql.connector"] = connector_stub

import InsertionFormula
from Patient import Patient
import UserRequest


VALID = {
    "patient_id": "A123456789",
    "first_name": "Avery",
    "last_name": "Morgan",
    "date_of_birth": "1990-04-12",
}


class RegistrationTests(unittest.TestCase):
    def setUp(self):
        UserRequest.clinic_state.in_queue = []
        UserRequest.clinic_state.current_patient = None

    def tearDown(self):
        UserRequest.clinic_state.in_queue = []
        UserRequest.clinic_state.current_patient = None

    def test_registration_only_does_not_queue_patient(self):
        with patch.object(InsertionFormula, "insert_patient", return_value=VALID["patient_id"]) as insert:
            result = UserRequest.register_new_patient(VALID)
        insert.assert_called_once_with(VALID)
        self.assertEqual(result["code"], "registered")
        self.assertEqual(UserRequest.clinic_state.in_queue, [])

    def test_registration_and_check_in_updates_queue(self):
        with patch.object(InsertionFormula, "insert_patient", return_value=VALID["patient_id"]):
            result = UserRequest.register_new_patient(VALID, check_in=True)
        self.assertEqual(result["code"], "registered_and_checked_in")
        self.assertEqual([patient.id for patient in UserRequest.clinic_state.in_queue], [VALID["patient_id"]])

    def test_lowercase_registration_is_persisted_in_uppercase(self):
        lowercase = dict(VALID, patient_id="  a123456789  ")
        with patch.object(InsertionFormula, "insert_patient", return_value=VALID["patient_id"]) as insert:
            result = UserRequest.register_new_patient(lowercase)
        insert.assert_called_once_with(VALID)
        self.assertEqual(result["patient"]["patient_id"], VALID["patient_id"])

    def test_failed_persistence_is_not_reported_or_queued(self):
        with patch.object(InsertionFormula, "insert_patient", side_effect=RuntimeError("database failed")):
            with self.assertRaisesRegex(RuntimeError, "database failed"):
                UserRequest.register_new_patient(VALID, check_in=True)
        self.assertEqual(UserRequest.clinic_state.in_queue, [])

    def test_invalid_registration_never_reaches_persistence(self):
        invalid = dict(VALID, date_of_birth="2024-31-99")
        with patch.object(InsertionFormula, "insert_patient") as insert:
            with self.assertRaisesRegex(ValueError, "Invalid date format"):
                UserRequest.register_new_patient(invalid)
        insert.assert_not_called()

    def test_existing_patient_check_in_and_duplicate_protection(self):
        patient = Patient(**VALID)
        with patch.object(UserRequest.PipeLineObject, "get_patient_profile", return_value=patient):
            first = UserRequest.check_in_existing_patient(VALID["patient_id"])
            duplicate = UserRequest.check_in_existing_patient(VALID["patient_id"])
        self.assertTrue(first["ok"])
        self.assertEqual(duplicate["code"], "duplicate")
        self.assertEqual(len(UserRequest.clinic_state.in_queue), 1)

    def test_lowercase_check_in_uses_canonical_lookup(self):
        patient = Patient(**dict(VALID, patient_id="a123456789"))
        with patch.object(UserRequest.PipeLineObject, "get_patient_profile", return_value=patient) as lookup:
            result = UserRequest.check_in_existing_patient(" a123456789 ")
        lookup.assert_called_once_with(VALID["patient_id"])
        self.assertEqual(result["patient"]["patient_id"], VALID["patient_id"])

    def test_lowercase_profile_search_uses_canonical_lookup(self):
        patient = Patient(**dict(VALID, patient_id="a123456789"))
        with patch.object(UserRequest.PipeLineObject, "get_patient_profile", return_value=patient) as lookup:
            profile = UserRequest.get_patient_profile_data("a123456789")
        lookup.assert_called_once_with(VALID["patient_id"])
        self.assertEqual(profile["patient_id"], VALID["patient_id"])

    def test_patient_id_normalization_preserves_validation(self):
        self.assertEqual(UserRequest.normalize_patient_id(" a123456789 "), VALID["patient_id"])
        self.assertEqual(UserRequest.normalize_patient_id(VALID["patient_id"]), VALID["patient_id"])
        self.assertEqual(UserRequest.validate_patient_id("a123456789"), VALID["patient_id"])
        for malformed in ("", "A123", "1123456789", "AA23456789", "A12345678!"):
            with self.subTest(patient_id=malformed):
                with self.assertRaises(ValueError):
                    UserRequest.validate_patient_id(malformed)

    def test_insert_patient_raises_when_query_reports_failure(self):
        with patch.object(InsertionFormula, "execute_query", return_value=None):
            with self.assertRaisesRegex(RuntimeError, "was not saved"):
                InsertionFormula.insert_patient(VALID)

    def test_insert_patient_accepts_zero_lastrowid_for_string_primary_key(self):
        with patch.object(InsertionFormula, "execute_query", return_value=0):
            self.assertEqual(InsertionFormula.insert_patient(VALID), VALID["patient_id"])


if __name__ == "__main__":
    unittest.main()
