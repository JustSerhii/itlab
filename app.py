from flask import Flask, render_template, request, jsonify, send_from_directory
from db_manager import dbManager
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
db_manager = dbManager()

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Web routes
@app.route('/')
def index():
    return render_template('index.html', tables=db_manager.get_table_name_list())

@app.route('/table/<int:table_index>')
def view_table(table_index):
    table = db_manager.get_table(table_index)
    if table:
        return render_template('table.html', table=table, table_index=table_index)
    return "Table not found", 404

@app.route('/join_tables', methods=['GET', 'POST'])
def join_tables():
    return render_template('join_tables.html', tables=db_manager.get_table_name_list())

# REST API routes
@app.route('/api/create_db', methods=['POST'])
def api_create_db():
    data = request.json
    if db_manager.create_db(data['db_name']):
        return jsonify(success=True, message="Database created successfully")
    return jsonify(success=False, message="Failed to create database"), 400

@app.route('/api/tables', methods=['GET', 'POST'])
def api_tables():
    if request.method == 'GET':
        return jsonify(tables=db_manager.get_table_name_list())
    elif request.method == 'POST':
        data = request.json
        if db_manager.add_table(data['table_name']):
            return jsonify(success=True, message="Table added successfully")
        return jsonify(success=False, message="Failed to add table"), 400

@app.route('/api/tables/<int:table_index>', methods=['GET', 'DELETE'])
def api_table(table_index):
    if request.method == 'GET':
        table = db_manager.get_table(table_index)
        if table:
            return jsonify(
                table_name=table.tName,
                columns=[(col.cName, col.typeName) for col in table.tColumnsList],
                rows=[row.rValuesList for row in table.tRowsList]
            )
        return jsonify(error="Table not found"), 404
    elif request.method == 'DELETE':
        if db_manager.delete_table(table_index):
            return jsonify(success=True, message="Table deleted successfully")
        return jsonify(success=False, message="Failed to delete table"), 400

@app.route('/api/tables/<int:table_index>/columns', methods=['POST'])
def api_add_column(table_index):
    data = request.json
    if db_manager.add_column(table_index, data['column_name'], data['column_type']):
        return jsonify(success=True, message="Column added successfully")
    return jsonify(success=False, message="Failed to add column"), 400

@app.route('/api/tables/<int:table_index>/columns/<int:column_index>', methods=['DELETE'])
def api_delete_column(table_index, column_index):
    if db_manager.delete_column(table_index, column_index):
        return jsonify(success=True, message="Column deleted successfully")
    return jsonify(success=False, message="Failed to delete column"), 400

@app.route('/api/tables/<int:table_index>/rows', methods=['POST'])
def api_add_row(table_index):
    data = request.json
    success, message = db_manager.add_row(table_index, data['row_values'])
    if success:
        return jsonify(success=True, message=message)
    return jsonify(success=False, message=message), 400

@app.route('/api/tables/<int:table_index>/rows/<int:row_index>', methods=['DELETE', 'PUT'])
def api_row_operations(table_index, row_index):
    if request.method == 'DELETE':
        if db_manager.delete_row(table_index, row_index):
            return jsonify(success=True, message="Row deleted successfully")
        return jsonify(success=False, message="Failed to delete row"), 400
    elif request.method == 'PUT':
        data = request.json
        if db_manager.update_row(table_index, row_index, data['row_values']):
            return jsonify(success=True, message="Row updated successfully")
        return jsonify(success=False, message="Failed to update row"), 400

@app.route('/api/save_db', methods=['POST'])
def api_save_db():
    data = request.json
    filename = secure_filename(data['file_path'])

    # Додаємо розширення .db, якщо користувач його не вказав
    if not filename.endswith('.db'):
        filename += '.db'

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # Save the database here (dbManager.save_db logic should be called)

    # Placeholder for save logic
    if db_manager.save_db(file_path):  # Переконайтеся, що save_db() працює як потрібно
        return jsonify(success=True, message="Database saved successfully", file_path=filename)

    return jsonify(success=False, message="Failed to save database"), 400

@app.route('/api/open_db', methods=['POST'])
def api_open_db():
    if 'file' not in request.files:
        return jsonify(success=False, message="No file part"), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(success=False, message="No selected file"), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        if db_manager.open_db(file_path):
            return jsonify(success=True, message="Database opened successfully")
    return jsonify(success=False, message="Failed to open database"), 400

@app.route('/api/join_tables', methods=['POST'])
def api_join_tables():
    data = request.json
    success, message, joined_data = db_manager.join_tables(
        int(data['table1_index']), int(data['table2_index']), data['column1_name'], data['column2_name']
    )
    if success:
        return jsonify(success=True, message=message, joined_data=joined_data)
    return jsonify(success=False, message=message), 400

if __name__ == '__main__':
    app.run(debug=True)
