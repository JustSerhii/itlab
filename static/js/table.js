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
    const target = e.target;

    // Якщо це клітинка (і не кнопка)
    if (target.tagName === 'TD' && !target.closest('button')) {
        const rowIndex = target.closest('tr').querySelector('.edit-row').dataset.rowIndex; // отримуємо індекс рядка
        const cellIndex = Array.from(target.parentNode.children).indexOf(target); // індекс клітинки

        if (!target.isContentEditable) {
            target.setAttribute('contenteditable', 'true');
            target.focus();
        }

        target.addEventListener('blur', async () => {
            target.setAttribute('contenteditable', 'false'); // закінчуємо редагування після втрати фокусу

            // Отримуємо всі значення з рядка
            const cells = Array.from(target.closest('tr').querySelectorAll('td:not(:last-child)')); // всі, крім останньої клітинки з кнопками
            const newValues = cells.map(cell => cell.textContent.trim());

            // Відправляємо оновлені значення на сервер
            const response = await fetch(`/api/tables/${tableIndex}/rows/${rowIndex}`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ row_values: newValues })
            });

            const result = await response.json();
            if (result.success) {
                alert('Row updated successfully');
            } else {
                alert(result.message);
            }
        });
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