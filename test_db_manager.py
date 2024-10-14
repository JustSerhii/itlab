import unittest
from db_manager import dbManager, DataType

class TestDBManager(unittest.TestCase):

    def setUp(self):
        # Створюємо об'єкт dbManager перед кожним тестом
        self.db = dbManager()
        self.db.create_db('TestDB')

    def test_create_db(self):
        self.assertEqual(self.db.db.name, 'TestDB')
        self.assertEqual(len(self.db.tables), 0)

    def test_add_table(self):
        self.assertTrue(self.db.add_table('Employees'))
        self.assertEqual(len(self.db.tables), 1)
        self.assertEqual(self.db.tables[0].tName, 'Employees')

    def test_add_duplicate_table(self):
        self.db.add_table('Employees')
        self.assertFalse(self.db.add_table('Employees'))

    def test_delete_table(self):
        self.db.add_table('Employees')
        self.assertTrue(self.db.delete_table(0))
        self.assertEqual(len(self.db.tables), 0)

    def test_delete_invalid_table(self):
        self.assertFalse(self.db.delete_table(0))

    def test_add_column(self):
        self.db.add_table('Employees')
        self.assertTrue(self.db.add_column(0, 'Name', DataType.STRING))
        self.assertEqual(len(self.db.tables[0].tColumnsList), 1)
        self.assertEqual(self.db.tables[0].tColumnsList[0].cName, 'Name')

    def test_add_multiple_columns(self):
        self.db.add_table('Employees')
        self.assertTrue(self.db.add_column(0, 'Name', DataType.STRING))
        self.assertTrue(self.db.add_column(0, 'Age', DataType.INTEGER))
        self.assertEqual(len(self.db.tables[0].tColumnsList), 2)

    def test_add_row(self):
        self.db.add_table('Employees')
        self.db.add_column(0, 'Name', DataType.STRING)
        success, message = self.db.add_row(0, ['Alice'])
        self.assertTrue(success)
        self.assertEqual(len(self.db.tables[0].tRowsList), 1)
        self.assertEqual(self.db.tables[0].tRowsList[0].rValuesList[0], 'Alice')

    def test_add_invalid_row(self):
        self.db.add_table('Employees')
        self.db.add_column(0, 'Name', DataType.STRING)
        self.db.add_column(0, 'Age', DataType.INTEGER)
        success, message = self.db.add_row(0, ['Alice', 'invalid_age'])
        self.assertFalse(success)
        self.assertIn('Invalid value for Integer', message)

    def test_update_row(self):
        self.db.add_table('Employees')
        self.db.add_column(0, 'Name', DataType.STRING)
        self.db.add_row(0, ['Alice'])
        self.assertTrue(self.db.update_row(0, 0, ['Bob']))
        self.assertEqual(self.db.tables[0].tRowsList[0].rValuesList[0], 'Bob')

    def test_update_invalid_row(self):
        self.db.add_table('Employees')
        self.db.add_column(0, 'Name', DataType.STRING)
        self.db.add_row(0, ['Alice'])
        self.assertFalse(self.db.update_row(0, 1, ['Bob']))  # Рядок не існує

    def test_delete_row(self):
        self.db.add_table('Employees')
        self.db.add_column(0, 'Name', DataType.STRING)
        self.db.add_row(0, ['Alice'])
        self.assertTrue(self.db.delete_row(0, 0))
        self.assertEqual(len(self.db.tables[0].tRowsList), 0)

    def test_delete_invalid_row(self):
        self.db.add_table('Employees')
        self.assertFalse(self.db.delete_row(0, 0))

    def test_add_color_column(self):
        self.db.add_table('Employees')
        self.assertTrue(self.db.add_column(0, 'FavoriteColor', DataType.COLOR))
        self.assertEqual(self.db.tables[0].tColumnsList[0].cName, 'FavoriteColor')

    def test_add_color_value(self):
        self.db.add_table('Employees')
        self.db.add_column(0, 'FavoriteColor', DataType.COLOR)
        success, message = self.db.add_row(0, ['#FF5733'])
        self.assertTrue(success)
        self.assertEqual(self.db.tables[0].tRowsList[0].rValuesList[0], '#FF5733')

    def test_add_invalid_color_value(self):
        self.db.add_table('Employees')
        self.db.add_column(0, 'FavoriteColor', DataType.COLOR)
        success, message = self.db.add_row(0, ['invalid_color'])
        self.assertFalse(success)
        self.assertIn('Invalid color format', message)

    def test_join_tables(self):
        self.db.add_table('Employees')
        self.db.add_column(0, 'ID', DataType.INTEGER)
        self.db.add_row(0, [1])

        self.db.add_table('Salaries')
        self.db.add_column(1, 'ID', DataType.INTEGER)
        self.db.add_column(1, 'Salary', DataType.INTEGER)
        self.db.add_row(1, [1, 5000])

        success, message, joined_data = self.db.join_tables(0, 1, 'ID', 'ID')
        self.assertTrue(success)
        self.assertEqual(joined_data[1], [1, 5000])  # Об'єднання без дублювання колонки ID

    def test_join_tables_invalid_columns(self):
        self.db.add_table('Employees')
        self.db.add_column(0, 'ID', DataType.INTEGER)
        self.db.add_row(0, [1])
        self.db.add_table('Salaries')
        self.db.add_column(1, 'ID', DataType.INTEGER)
        success, message, joined_data = self.db.join_tables(0, 1, 'invalid_column', 'ID')
        self.assertFalse(success)
        self.assertIn('Specified columns not found', message)


if __name__ == '__main__':
    unittest.main()
