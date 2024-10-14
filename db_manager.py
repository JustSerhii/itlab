import pickle


class dbManager:
    def __init__(self):
        self.db = None
        self.tables = []

    def create_db(self, db_name):
        self.db = Database(db_name)
        return True

    def add_table(self, table_name):
        if not table_name:
            return False
        if any(table.tName == table_name for table in self.tables):
            return False
        new_table = Table(table_name)
        self.tables.append(new_table)
        return True

    def delete_table(self, table_index):
        if 0 <= table_index < len(self.tables):
            del self.tables[table_index]
            return True
        return False

    def get_table(self, table_index):
        if table_index is None:
            return None
        if 0 <= table_index < len(self.tables):
            return self.tables[table_index]
        return None

    def get_table_name_list(self):
        return [table.tName for table in self.tables]

    def add_column(self, table_index, column_name, column_type):
        table = self.get_table(table_index)
        if table:
            new_column = Column(column_name, column_type)
            table.tColumnsList.append(new_column)
            return True
        return False

    def delete_column(self, table_index, column_index):
        table = self.get_table(table_index)
        if table and 0 <= column_index < len(table.tColumnsList):
            del table.tColumnsList[column_index]
            for row in table.tRowsList:
                del row.rValuesList[column_index]
            return True
        return False

    def add_row(self, table_index, row_values):
        table = self.get_table(table_index)
        if table:
            if len(row_values) == len(table.tColumnsList):
                new_row = Row(row_values)
                table.tRowsList.append(new_row)
                return True
        return False

    def delete_row(self, table_index, row_index):
        table = self.get_table(table_index)
        if table and 0 <= row_index < len(table.tRowsList):
            del table.tRowsList[row_index]
            return True
        return False

    def update_row(self, table_index, row_index, new_values):
        table = self.get_table(table_index)
        if table and 0 <= row_index < len(table.tRowsList):
            if len(new_values) == len(table.tColumnsList):
                table.tRowsList[row_index].rValuesList = new_values
                return True
        return False

    def change_value(self, new_value, table_index, column_index, row_index):
        table = self.get_table(table_index)
        if table and 0 <= column_index < len(table.tColumnsList) and 0 <= row_index < len(table.tRowsList):
            table.tRowsList[row_index].rValuesList[column_index] = new_value
            return True
        return False

    def save_db(self, path):
        try:
            with open(path, 'wb') as file:
                pickle.dump((self.db, self.tables), file)
            return True
        except Exception as e:
            print(f"Error saving database: {e}")
            return False

    def open_db(self, path):
        try:
            with open(path, 'rb') as file:
                self.db, self.tables = pickle.load(file)
            return True
        except Exception as e:
            print(f"Error opening database: {e}")
            return False

class Database:
    def __init__(self, name):
        self.name = name

class Table:
    def __init__(self, name):
        self.tName = name
        self.tColumnsList = []
        self.tRowsList = []

class Column:
    def __init__(self, name, type_name):
        self.cName = name
        self.typeName = type_name

class Row:
    def __init__(self, values):
        self.rValuesList = values