import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from db_manager import dbManager

class DBApp:
    def __init__(self, root):
        self.db_manager = dbManager()
        self.root = root
        self.root.title("Database Manager")
        self.root.geometry("800x600")

        self.create_widgets()
        self.current_table_index = None
        self.data_widgets = []

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Database controls
        db_frame = ttk.LabelFrame(main_frame, text="Database", padding="5")
        db_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.db_name_entry = ttk.Entry(db_frame)
        self.db_name_entry.grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(db_frame, text="Create DB", command=self.create_db).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(db_frame, text="Save DB", command=self.save_db).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(db_frame, text="Open DB", command=self.open_db).grid(row=0, column=3, padx=5, pady=5)

        # Table controls
        table_frame = ttk.LabelFrame(main_frame, text="Tables", padding="5")
        table_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        self.table_name_entry = ttk.Entry(table_frame)
        self.table_name_entry.grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(table_frame, text="Add Table", command=self.add_table).grid(row=0, column=1, padx=5, pady=5)

        self.table_listbox = tk.Listbox(table_frame)
        self.table_listbox.grid(row=1, column=0, columnspan=2, sticky=(tk.N, tk.S, tk.W, tk.E), padx=5, pady=5)
        self.table_listbox.bind('<<ListboxSelect>>', self.on_table_select)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(1, weight=1)

        ttk.Button(table_frame, text="Delete Table", command=self.delete_table).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Column and data frame
        self.data_frame = ttk.Frame(main_frame)
        self.data_frame.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        main_frame.columnconfigure(1, weight=3)

        # Column controls
        column_frame = ttk.LabelFrame(self.data_frame, text="Columns", padding="5")
        column_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        self.column_name_entry = ttk.Entry(column_frame)
        self.column_name_entry.grid(row=0, column=0, padx=5, pady=5)

        self.column_type = tk.StringVar(value="Integer")
        ttk.OptionMenu(column_frame, self.column_type, "Integer", "Integer", "Real", "Char", "String", "Path", "ColorInvl").grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(column_frame, text="Add Column", command=self.add_column).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(column_frame, text="Delete Column", command=self.delete_column).grid(row=0, column=3, padx=5, pady=5)

        # Data display area
        self.data_display = ttk.Frame(self.data_frame)
        self.data_display.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.data_frame.rowconfigure(1, weight=1)
        self.data_frame.columnconfigure(0, weight=1)

        # Scrollbars for data display
        self.vsb = ttk.Scrollbar(self.data_frame, orient="vertical")
        self.vsb.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.hsb = ttk.Scrollbar(self.data_frame, orient="horizontal")
        self.hsb.grid(row=2, column=0, sticky=(tk.W, tk.E))

        # Row controls
        row_frame = ttk.Frame(self.data_frame)
        row_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        ttk.Button(row_frame, text="Add Row", command=self.add_row).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(row_frame, text="Delete Row", command=self.delete_row).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(row_frame, text="Save Changes", command=self.save_changes).grid(row=0, column=2, padx=5, pady=5)

        ttk.Button(self.data_frame, text="Join Tables", command=self.join_tables).grid(row=4, column=0, padx=5, pady=5)

    def create_db(self):
        db_name = self.db_name_entry.get()
        if self.db_manager.create_db(db_name):
            messagebox.showinfo("Success", "Database created successfully")
            self.update_table_listbox()

    def add_table(self):
        table_name = self.table_name_entry.get().strip()
        if table_name:  # Перевіряємо, чи не порожнє ім'я таблиці
            if self.db_manager.add_table(table_name):
                self.update_table_listbox()
                self.table_name_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to add table")
        else:
            messagebox.showerror("Error", "Table name cannot be empty")

    def delete_table(self):
        selected_indices = self.table_listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            self.db_manager.delete_table(index)
            self.update_table_listbox()
            self.clear_data_display()
        else:
            messagebox.showerror("Error", "No table selected to delete.")

    def add_column(self):
        if self.current_table_index is not None:
            column_name = self.column_name_entry.get()
            column_type = self.column_type.get()
            if self.db_manager.add_column(self.current_table_index, column_name, column_type):
                messagebox.showinfo("Success", "Column added successfully")
                self.update_data_display()
                self.column_name_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to add column")
        else:
            messagebox.showerror("Error", "No table selected")

    def add_row(self):
        if self.current_table_index is not None:
            table = self.db_manager.get_table(self.current_table_index)
            if not table.tColumnsList:
                messagebox.showerror("Error", "Table has no columns. Add columns before adding rows.")
                return
            new_row_values = []
            for col in table.tColumnsList:
                if col.typeName == "ColorInvl":
                    # Only ask for one color, assuming it is an RGB code in the format "#RRGGBB"
                    value = simpledialog.askstring("Add Row", f"Enter color value for {col.cName} ({col.typeName}):")
                    if value is None or not self.is_valid_color(value):  # Check for valid color input
                        return
                    new_row_values.append(value)
                else:
                    value = simpledialog.askstring("Add Row", f"Enter value for {col.cName} ({col.typeName}):")
                    if value is None:  # User canceled
                        return
                    new_row_values.append(value)
            success, message = self.db_manager.add_row(self.current_table_index, new_row_values)
            if success:
                self.update_data_display()
            else:
                messagebox.showerror("Error", message)

    def is_valid_color(self, value):
        # Check if the value matches the format of a hex color code
        return isinstance(value, str) and len(value) == 7 and value.startswith('#')

    def join_tables(self):
        if len(self.db_manager.tables) < 2:
            messagebox.showerror("Error", "Need at least two tables to join")
            return

        table1_index = simpledialog.askinteger("Join Tables", "Enter index of first table:", minvalue=0,
                                               maxvalue=len(self.db_manager.tables) - 1)
        table2_index = simpledialog.askinteger("Join Tables", "Enter index of second table:", minvalue=0,
                                               maxvalue=len(self.db_manager.tables) - 1)

        if table1_index is None or table2_index is None:
            return

        table1 = self.db_manager.get_table(table1_index)
        table2 = self.db_manager.get_table(table2_index)

        column1_name = simpledialog.askstring("Join Tables", f"Enter column name from {table1.tName}:")
        column2_name = simpledialog.askstring("Join Tables", f"Enter column name from {table2.tName}:")

        if column1_name and column2_name:
            success, message, joined_data = self.db_manager.join_tables(table1_index, table2_index, column1_name,
                                                                        column2_name)
            if success:
                self.display_joined_data(joined_data)
            else:
                messagebox.showerror("Error", message)

    def display_joined_data(self, joined_data):
        # Створюємо нове вікно для відображення об'єднаних даних
        joined_window = tk.Toplevel(self.root)
        joined_window.title("Joined Table Data")

        # Створюємо TreeView для відображення даних
        tree = ttk.Treeview(joined_window)
        tree["columns"] = joined_data[0]
        tree["show"] = "headings"

        # Налаштовуємо заголовки стовпців
        for column in joined_data[0]:
            tree.heading(column, text=column)
            tree.column(column, width=100)

        # Додаємо дані
        for row in joined_data[1:]:
            tree.insert("", "end", values=row)

        # Додаємо прокрутку
        scrollbar = ttk.Scrollbar(joined_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Розміщуємо віджети
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def delete_column(self):
        if self.current_table_index is not None:
            column_name = simpledialog.askstring("Delete Column", "Enter column name to delete:")
            if column_name:
                table = self.db_manager.get_table(self.current_table_index)
                for i, col in enumerate(table.tColumnsList):
                    if col.cName == column_name:
                        self.db_manager.delete_column(self.current_table_index, i)
                        self.update_data_display()
                        messagebox.showinfo("Success", f"Column '{column_name}' deleted successfully")
                        return
                messagebox.showerror("Error", f"Column '{column_name}' not found")
        else:
            messagebox.showerror("Error", "No table selected")

    def delete_row(self):
        if self.current_table_index is not None:
            row_index = simpledialog.askinteger("Delete Row", "Enter row number to delete:")
            if row_index is not None:
                if self.db_manager.delete_row(self.current_table_index, row_index - 1):  # Adjust for 0-based index
                    self.update_data_display()
                else:
                    messagebox.showerror("Error", f"Failed to delete row {row_index}")
        else:
            messagebox.showerror("Error", "No table selected")

    def save_changes(self):
        if self.current_table_index is not None:
            table = self.db_manager.get_table(self.current_table_index)
            for row_index, row_widgets in enumerate(self.data_widgets[1:]):  # Skip header row
                new_values = [entry.get() for entry in row_widgets]
                self.db_manager.update_row(self.current_table_index, row_index, new_values)
            messagebox.showinfo("Success", "Changes saved successfully")
            self.update_data_display()
        else:
            messagebox.showerror("Error", "No table selected")

    def update_data_display(self):
        self.clear_data_display()

        if self.current_table_index is not None:
            table = self.db_manager.get_table(self.current_table_index)
            if table:
                # Create header
                header_row = []
                for col in table.tColumnsList:
                    entry = ttk.Entry(self.data_display, width=15)
                    entry.insert(0, col.cName)
                    entry.configure(state='readonly')
                    header_row.append(entry)
                self.data_widgets.append(header_row)

                # Create data rows
                for row in table.tRowsList:
                    row_widgets = []
                    for value in row.rValuesList:
                        entry = ttk.Entry(self.data_display, width=15)
                        entry.insert(0, str(value))
                        row_widgets.append(entry)
                    self.data_widgets.append(row_widgets)

                # Place widgets in grid
                for i, row in enumerate(self.data_widgets):
                    for j, widget in enumerate(row):
                        widget.grid(row=i, column=j, padx=1, pady=1, sticky=(tk.W, tk.E))

                # Configure scrollbars
                self.data_display.update_idletasks()
                self.vsb.configure(command=self.data_display.yview)
                self.hsb.configure(command=self.data_display.xview)
                self.data_display.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

    def clear_data_display(self):
        for row in self.data_widgets:
            for widget in row:
                widget.destroy()
        self.data_widgets = []

    def update_table_listbox(self):
        self.table_listbox.delete(0, tk.END)
        for table_name in self.db_manager.get_table_name_list():
            self.table_listbox.insert(tk.END, table_name)

    def on_table_select(self, event):
        selected_indices = self.table_listbox.curselection()
        if selected_indices:
            self.current_table_index = selected_indices[0]
            self.update_data_display()
        else:
            self.current_table_index = None
            self.clear_data_display()

    def save_db(self):
        if self.db_manager.db:
            path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("Database Files", "*.db")])
            if path:
                if self.db_manager.save_db(path):
                    messagebox.showinfo("Success", "Database saved successfully")
                else:
                    messagebox.showerror("Error", "Failed to save database")
        else:
            messagebox.showerror("Error", "No database to save")

    def open_db(self):
        path = filedialog.askopenfilename(filetypes=[("Database Files", "*.db")])
        if path:
            self.db_manager.open_db(path)
            self.update_table_listbox()
            self.clear_data_display()
            messagebox.showinfo("Success", "Database opened successfully")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = DBApp(root)
    root.mainloop()