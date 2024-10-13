import unittest
from db_manager import dbManager

class TestDBManager(unittest.TestCase):
    def setUp(self):
        self.manager = dbManager()
        self.manager.create_db("TestDB")
        self.manager.add_table("TestTable")

    def test_create_db(self):
        # Тест створення бази даних
        self.assertTrue(self.manager.create_db("NewTestDB"))
        self.assertEqual(self.manager.db.dbName, "NewTestDB")

    def test_add_table(self):
        # Тест додавання таблиці
        self.assertTrue(self.manager.add_table("AnotherTable"))
        self.assertEqual(len(self.manager.db.dbTablesList), 2)
        self.assertEqual(self.manager.db.dbTablesList[1].tName, "AnotherTable")

    def test_add_column(self):
        # Тест додавання колонки
        self.assertTrue(self.manager.add_column(0, "TestColumn", "Integer"))
        self.assertEqual(len(self.manager.db.dbTablesList[0].tColumnsList), 1)
        self.assertEqual(self.manager.db.dbTablesList[0].tColumnsList[0].cName, "TestColumn")

    def test_add_row(self):
        # Тест додавання рядка
        self.manager.add_column(0, "TestColumn", "Integer")
        self.assertTrue(self.manager.add_row(0))
        self.assertEqual(len(self.manager.db.dbTablesList[0].tRowsList), 1)

    def test_change_value(self):
        # Тест зміни значення
        self.manager.add_column(0, "TestColumn", "Integer")
        self.manager.add_row(0)
        self.assertTrue(self.manager.change_value("123", 0, 0, 0))
        self.assertEqual(self.manager.db.dbTablesList[0].tRowsList[0].rValuesList[0], "123")

    def test_custom_column_validation(self):
        # Тест валідації для ColorInvl
        self.manager.add_column(0, "Interval", "ColorInvl")
        self.manager.add_row(0)
        self.assertTrue(self.manager.change_value("5 10", 0, 0, 0))  # Valid interval
        self.assertFalse(self.manager.change_value("10 5", 0, 0, 0))  # Invalid interval

    def test_delete_row(self):
        # Тест видалення рядка
        self.manager.add_column(0, "TestColumn", "Integer")
        self.manager.add_row(0)
        self.manager.add_row(0)
        self.manager.delete_row(0, 1)
        self.assertEqual(len(self.manager.db.dbTablesList[0].tRowsList), 1)

    def test_delete_column(self):
        # Тест видалення колонки
        self.manager.add_column(0, "TestColumn1", "Integer")
        self.manager.add_column(0, "TestColumn2", "Real")
        self.manager.add_row(0)
        self.manager.delete_column(0, 1)
        self.assertEqual(len(self.manager.db.dbTablesList[0].tColumnsList), 1)
        self.assertEqual(self.manager.db.dbTablesList[0].tColumnsList[0].cName, "TestColumn1")

    def test_delete_table(self):
        # Тест видалення таблиці
        self.manager.add_table("AnotherTable")
        self.manager.delete_table(1)
        self.assertEqual(len(self.manager.db.dbTablesList), 1)

    def test_save_and_open_db(self):
        # Тест збереження та відкриття бази даних
        self.manager.add_column(0, "TestColumn", "Integer")
        self.manager.add_row(0)
        self.manager.change_value("456", 0, 0, 0)

        self.manager.save_db("test_db.txt")

        new_manager = dbManager()
        new_manager.open_db("test_db.txt")
        self.assertEqual(new_manager.db.dbName, "TestDB")
        self.assertEqual(len(new_manager.db.dbTablesList), 1)
        self.assertEqual(len(new_manager.db.dbTablesList[0].tRowsList), 1)
        self.assertEqual(new_manager.db.dbTablesList[0].tRowsList[0].rValuesList[0], "456")

if __name__ == "__main__":
    unittest.main()
