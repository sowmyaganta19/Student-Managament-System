import unittest
import student_mgmt as sm

class TestStudentMgmt(unittest.TestCase):
    def setUp(self):
        # start with a clean in-memory list
        sm.students.clear()

    def test_add_and_search(self):
        ok = sm.add_student_record("101", "Alice", "A", "15")
        self.assertTrue(ok)
        s = sm.search_by_roll("101")
        self.assertIsNotNone(s)
        self.assertEqual(s["name"], "Alice")

    def test_duplicate_roll(self):
        self.assertTrue(sm.add_student_record("101", "Alice", "A"))
        self.assertFalse(sm.add_student_record("101", "Bob", "B"))

    def test_update(self):
        sm.add_student_record("102", "Bhavani", "B", "16")
        updated = sm.update_student_record("102", name="Bhavani R", grade="A")
        self.assertTrue(updated)
        s = sm.search_by_roll("102")
        self.assertEqual(s["name"], "Bhavani R")
        self.assertEqual(s["grade"], "A")

    def test_delete(self):
        sm.add_student_record("103", "Ajay", "C")
        deleted = sm.delete_student_record("103")
        self.assertTrue(deleted)
        self.assertIsNone(sm.search_by_roll("103"))

if __name__ == "__main__":
    unittest.main()
