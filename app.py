import _tkinter
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
        data_frame = ttk.Frame(main_frame)
        data_frame.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        main_frame.columnconfigure(1, weight=3)

        # Column controls
        column_frame = ttk.LabelFrame(data_frame, text="Columns", padding="5")
        column_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        self.column_name_entry = ttk.Entry(column_frame)
        self.column_name_entry.grid(row=0, column=0, padx=5, pady=5)

        self.column_type = tk.StringVar(value="Integer")
        ttk.OptionMenu(column_frame, self.column_type, "Integer", "Integer", "Real", "Char", "String", "Path", "ColorInvl").grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(column_frame, text="Add Column", command=self.add_column).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(column_frame, text="Delete Column", command=self.delete_column).grid(row=0, column=3, padx=5, pady=5)

        # Treeview for displaying columns and rows
        self.tree = ttk.Treeview(data_frame, style="Centered.Treeview")
        self.tree.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        data_frame.columnconfigure(0, weight=1)
        data_frame.rowconfigure(1, weight=1)

        # Scrollbars for Treeview
        vsb = ttk.Scrollbar(data_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=1, column=1, sticky=(tk.N, tk.S))
        hsb = ttk.Scrollbar(data_frame, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=2, column=0, sticky=(tk.W, tk.E))
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Row controls
        row_frame = ttk.Frame(data_frame)
        row_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        ttk.Button(row_frame, text="Add Row", command=self.add_row).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(row_frame, text="Delete Row", command=self.delete_row).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(row_frame, text="Edit Row", command=self.edit_row).grid(row=0, column=2, padx=5, pady=5)

        # Create a style for centered Treeview
        style = ttk.Style()
        style.configure("Centered.Treeview", justify="center")
        style.configure("Centered.Treeview.Heading", justify="center")

    def create_db(self):
        db_name = self.db_name_entry.get()
        if self.db_manager.create_db(db_name):
            messagebox.showinfo("Success", "Database created successfully")
            self.update_table_listbox()

    def add_table(self):
        table_name = self.table_name_entry.get()
        if self.db_manager.add_table(table_name):
            self.update_table_listbox()
            self.table_name_entry.delete(0, tk.END)

    def delete_table(self):
        selected_indices = self.table_listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            self.db_manager.delete_table(index)
            self.update_table_listbox()
            self.clear_treeview()
        else:
            messagebox.showerror("Error", "No table selected to delete.")

    def add_column(self):
        if self.current_table_index is not None:
            column_name = self.column_name_entry.get()
            column_type = self.column_type.get()
            if self.db_manager.add_column(self.current_table_index, column_name, column_type):
                messagebox.showinfo("Success", "Column added successfully")
                self.update_treeview()
                self.column_name_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to add column")
        else:
            messagebox.showerror("Error", "No table selected")

    def delete_column(self):
        if self.current_table_index is not None:
            column_name = simpledialog.askstring("Delete Column", "Enter column name to delete:")
            if column_name:
                table = self.db_manager.get_table(self.current_table_index)
                for i, col in enumerate(table.tColumnsList):
                    if col.cName == column_name:
                        self.db_manager.delete_column(self.current_table_index, i)
                        self.update_treeview()
                        messagebox.showinfo("Success", f"Column '{column_name}' deleted successfully")
                        return
                messagebox.showerror("Error", f"Column '{column_name}' not found")
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
                value = simpledialog.askstring("Add Row", f"Enter value for {col.cName} ({col.typeName}):")
                if value is None:  # User canceled
                    return
                new_row_values.append(value)
            if self.db_manager.add_row(self.current_table_index, new_row_values):
                self.update_treeview()
            else:
                messagebox.showerror("Error", "Failed to add row")
        else:
            messagebox.showerror("Error", "No table selected")

    def delete_row(self):
        if self.current_table_index is not None:
            selected_items = self.tree.selection()
            if selected_items:
                for item in reversed(selected_items):
                    row_index = int(self.tree.index(item))
                    if self.db_manager.delete_row(self.current_table_index, row_index):
                        self.tree.delete(item)
                    else:
                        messagebox.showerror("Error", f"Failed to delete row {row_index}")
            else:
                messagebox.showerror("Error", "No row selected to delete")
        else:
            messagebox.showerror("Error", "No table selected")

    def edit_row(self):
        if self.current_table_index is None:
            messagebox.showerror("Error", "No table selected. Please select a table first.")
            return

        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "No row selected to edit. Please select a row.")
            return

        item = selected_items[0]
        try:
            row_index = self.tree.index(item)
        except tk.TclError:
            messagebox.showerror("Error", "Selected item not found in the table.")
            return

        table = self.db_manager.get_table(self.current_table_index)
        if not table:
            messagebox.showerror("Error", "Selected table not found.")
            return

        values = self.tree.item(item, 'values')
        if not values:
            messagebox.showerror("Error", "Selected item has no values.")
            return

        new_row_values = []
        for i, col in enumerate(table.tColumnsList):
            current_value = values[i] if i < len(values) else ""
            new_value = simpledialog.askstring("Edit Row",
                                               f"Enter new value for {col.cName} ({col.typeName}):",
                                               initialvalue=current_value)
            if new_value is None:  # User canceled
                return
            # Add type conversion or validation if necessary
            new_row_values.append(new_value)

        if len(new_row_values) == len(table.tColumnsList):  # Ensure all values are provided
            if self.db_manager.update_row(self.current_table_index, row_index, new_row_values):
                self.update_treeview()
                messagebox.showinfo("Success", "Row updated successfully.")
            else:
                messagebox.showerror("Error", "Failed to update row. Please check your input.")
        else:
            messagebox.showerror("Error", "Number of values doesn't match the number of columns.")

    def update_treeview(self):
        self.clear_treeview()

        if self.current_table_index is not None:
            table = self.db_manager.get_table(self.current_table_index)
            if table:
                self.tree["columns"] = [col.cName for col in table.tColumnsList]
                self.tree.column("#0", width=0, stretch=tk.NO)
                for col in table.tColumnsList:
                    self.tree.heading(col.cName, text=col.cName, anchor=tk.CENTER)
                    self.tree.column(col.cName, width=100, stretch=tk.YES, anchor=tk.CENTER)

                for row in table.tRowsList:
                    self.tree.insert("", "end", values=row.rValuesList)

    def clear_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree["columns"] = ()

    def update_table_listbox(self):
        self.table_listbox.delete(0, tk.END)
        for table_name in self.db_manager.get_table_name_list():
            self.table_listbox.insert(tk.END, table_name)

    def on_table_select(self, event):
        selected_indices = self.table_listbox.curselection()
        if selected_indices:
            self.current_table_index = selected_indices[0]
            self.update_treeview()
        else:
            self.current_table_index = None
            self.clear_treeview()

    def save_db(self):
        if self.db_manager.db:
            path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("Database Files", "*.db")])
            if path:
                self.db_manager.save_db(path)
                messagebox.showinfo("Success", "Database saved successfully")
        else:
            messagebox.showerror("Error", "No database to save")

    def open_db(self):
        path = filedialog.askopenfilename(filetypes=[("Database Files", "*.db")])
        if path:
            self.db_manager.open_db(path)
            self.update_table_listbox()
            self.clear_treeview()
            messagebox.showinfo("Success", "Database opened successfully")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = DBApp(root)
    root.mainloop()