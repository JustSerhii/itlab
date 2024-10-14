document.addEventListener('DOMContentLoaded', (event) => {
    const addColumnForm = document.getElementById('add-column-form');
    const addRowForm = document.getElementById('add-row-form');
    const dataTable = document.getElementById('data-table');
    const deleteTableBtn = document.getElementById('delete-table-btn');
    const tableIndex = addColumnForm.elements['table_index'].value;

    addColumnForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const columnName = addColumnForm.elements['column_name'].value;
        const columnType = addColumnForm.elements['column_type'].value;
        const response = await fetch(`/api/tables/${tableIndex}/columns`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({column_name: columnName, column_type: columnType})
        });
        const result = await response.json();
        if (result.success) {
            location.reload();
        }
        alert(result.message);
    });

    addRowForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(addRowForm);
        const rowValues = formData.getAll('row_values[]');
        const response = await fetch(`/api/tables/${tableIndex}/rows`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({row_values: rowValues})
        });
        const result = await response.json();
        if (result.success) {
            location.reload();
        }
        alert(result.message);
    });

   dataTable.addEventListener('click', async (e) => {
    if (e.target.classList.contains('edit-row')) {
        const rowIndex = e.target.dataset.rowIndex;
        const row = e.target.closest('tr');
        const cells = row.querySelectorAll('td'); // отримати всі клітинки рядка
        const newValues = [];

        cells.forEach((cell, index) => {
            if (index < cells.length - 1) { // не враховувати клітинку з кнопками "Edit" і "Delete"
                const currentValue = cell.querySelector('.cell-data') ? cell.querySelector('.cell-data').textContent : cell.textContent;
                const newValue = prompt(`Enter new value for ${currentValue}:`, currentValue);
                newValues.push(newValue !== null ? newValue : currentValue);
            }
        });

        const response = await fetch(`/api/tables/${tableIndex}/rows/${rowIndex}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ row_values: newValues })
        });

        const result = await response.json();
        if (result.success) {
            location.reload();
        }
        alert(result.message);
    }
});

    deleteTableBtn.addEventListener('click', async () => {
        if (confirm('Are you sure you want to delete this table?')) {
            const response = await fetch(`/api/tables/${tableIndex}`, {
                method: 'DELETE',
                headers: {'Content-Type': 'application/json'}
            });
            const result = await response.json();
            if (result.success) {
                window.location.href = '/';
            }
            alert(result.message);
        }
    });
});