import unittest
import os
import sqlite3
from passwordmanager import passwordmanager as script

class TestFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.mp = "pw123"
        self.ts = "test-service"

        # Delete local db
        # in case db was created outside of tests
        db_file = os.getcwd() + "/pwm.db"
        if os.path.isfile(db_file):
            os.remove(db_file)

    @classmethod
    def tearDownClass(self):
        # Delete local db
        db_file = os.getcwd() + "/pwm.db"
        if os.path.isfile(db_file):
            os.remove(db_file)

    def check_db_entry(self):
        try:
            conn = sqlite3.connect("pwm.db")
            cursor = conn.execute("SELECT id, service, version, updated from SERVICES")

            rows = []
            for row in cursor:
                rows.append(row)

            conn.close()
            return rows

        except Exception as err:
            print("[!] Error: {}".format(err))
            exit(1)

    def test_01_add_new_password(self):
        script.add_new_password(self.mp, self.ts)

        # First row has to look like this
        expected_row = (1, self.ts, 1, script.date_today())
        rows = self.check_db_entry()
        for row in rows:
            self.assertEqual(row, expected_row)

    def test_02_change_password(self):
        script.change_password(self.mp, self.ts)

        # First row has to look like this
        expected_row = (1, self.ts, 2, script.date_today())
        rows = self.check_db_entry()
        for row in rows:
            self.assertEqual(row, expected_row)

    def test_03_get_version_of_service(self):
        version = script.get_version_of_service(self.ts)

        self.assertEqual(version, 2)

    def test_get_service(self):
        pass

    def test_get_master_password_and_service(self):
        pass

    def test_get_master_password_with_verification(self):
        pass

if __name__ == "__main__":
    unittest.main()
