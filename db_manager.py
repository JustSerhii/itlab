# db_manager.py
import pickle
from typing import List, Any, Tuple

class DataType:
    INTEGER = "Integer"
    REAL = "Real"
    CHAR = "Char"
    STRING = "String"
    COLOR = "Color"
    COLOR_INVL = "ColorInvl"

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
            for row in table.tRowsList:
                row.rValuesList.append(None)
            return True
        return False

    def validate_value(self, value, column_type):
        try:
            if column_type == DataType.INTEGER:
                return int(value)
            elif column_type == DataType.REAL:
                return float(value)
            elif column_type == DataType.CHAR:
                return str(value)[0] if value else ''
            elif column_type == DataType.STRING:
                return str(value)
            elif column_type == DataType.COLOR:
                if not (isinstance(value, str) and len(value) == 7 and value.startswith('#')):
                    raise ValueError("Invalid color format. Use #RRGGBB")
                return value
            elif column_type == DataType.COLOR_INVL:
                # Expecting a string format: '#RRGGBB,#RRGGBB'
                if not isinstance(value, str) or ',' not in value:
                    raise ValueError("ColorInvl must be a string in the format '#RRGGBB,#RRGGBB'")

                color1, color2 = value.split(',')
                # Validate both colors
                color1 = self.validate_value(color1.strip(), DataType.COLOR)
                color2 = self.validate_value(color2.strip(), DataType.COLOR)
                return (color1, color2)  # Return as a tuple of two colors
            else:
                raise ValueError(f"Unknown data type: {column_type}")
        except ValueError as e:
            raise ValueError(f"Invalid value for {column_type}: {e}")

    def add_row(self, table_index, row_values):
        table = self.get_table(table_index)
        if table:
            # Find the "ID" column by name (case-insensitive)
            id_column_index = next((i for i, col in enumerate(table.tColumnsList) if col.cName.lower() == 'id'), None)

            if id_column_index is not None:
                new_id = row_values[id_column_index]

                # Check if the new "ID" value already exists in the table
                for row in table.tRowsList:
                    if row.rValuesList[id_column_index] == new_id:
                        return False, f"Error: Duplicate ID value '{new_id}' already exists. Please choose a unique ID."

            # Validate and add the new row if all values are correct
            if len(row_values) == len(table.tColumnsList):
                validated_values = []
                for value, column in zip(row_values, table.tColumnsList):
                    try:
                        validated_value = self.validate_value(value, column.typeName)
                        validated_values.append(validated_value)
                    except ValueError as e:
                        return False, str(e)
                new_row = Row(validated_values)
                table.tRowsList.append(new_row)
                return True, "Row added successfully"
        return False, "Failed to add row"

    def join_tables(self, table1_index: int, table2_index: int, column1_name: str, column2_name: str) -> Tuple[bool, str, List[List[Any]]]:
        table1 = self.get_table(table1_index)
        table2 = self.get_table(table2_index)

        if not table1 or not table2:
            return False, "One or both tables do not exist", []

        column1_index = next((i for i, col in enumerate(table1.tColumnsList) if col.cName == column1_name), None)
        column2_index = next((i for i, col in enumerate(table2.tColumnsList) if col.cName == column2_name), None)

        if column1_index is None or column2_index is None:
            return False, "Specified columns not found in tables", []

        joined_data = []
        header = [f"{table1.tName}.{col.cName}" for col in table1.tColumnsList] + \
                 [f"{table2.tName}.{col.cName}" for col in table2.tColumnsList if col.cName != column2_name]
        joined_data.append(header)

        for row1 in table1.tRowsList:
            for row2 in table2.tRowsList:
                if row1.rValuesList[column1_index] == row2.rValuesList[column2_index]:
                    joined_row = row1.rValuesList + [v for i, v in enumerate(row2.rValuesList) if i != column2_index]
                    joined_data.append(joined_row)

        return True, "Tables joined successfully", joined_data

    def delete_column(self, table_index, column_index):
        table = self.get_table(table_index)
        if table and 0 <= column_index < len(table.tColumnsList):
            del table.tColumnsList[column_index]
            for row in table.tRowsList:
                del row.rValuesList[column_index]
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
                validated_values = []
                for value, column in zip(new_values, table.tColumnsList):
                    try:
                        validated_value = self.validate_value(value, column.typeName)
                        validated_values.append(validated_value)
                    except ValueError as e:
                        return False
                table.tRowsList[row_index].rValuesList = validated_values
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