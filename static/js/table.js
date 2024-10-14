document.addEventListener('DOMContentLoaded', (event) => {
    const addColumnForm = document.getElementById('add-column-form');
    const addRowForm = document.getElementById('add-row-form');
    const dataTable = document.getElementById('data-table');
    const deleteTableBtn = document.getElementById('delete-table-btn');
    const tableIndex = addColumnForm.elements['table_index'].value;
    const messageBox = document.createElement('div');

    // Додаємо повідомлення про успішні операції
    document.body.appendChild(messageBox);
    messageBox.style.position = 'fixed';
    messageBox.style.top = '10px';
    messageBox.style.right = '10px';
    messageBox.style.padding = '10px';
    messageBox.style.backgroundColor = '#4caf50';
    messageBox.style.color = '#fff';
    messageBox.style.display = 'none';

    function showMessage(message) {
        messageBox.textContent = message;
        messageBox.style.display = 'block';
        setTimeout(() => {
            messageBox.style.display = 'none';
        }, 2000);
    }

    // Додаємо колонку
    addColumnForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const columnName = addColumnForm.elements['column_name'].value;
        const columnType = addColumnForm.elements['column_type'].value;
        const response = await fetch(`/api/tables/${tableIndex}/columns`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ column_name: columnName, column_type: columnType })
        });
        const result = await response.json();
        if (result.success) {
            location.reload(); // перезавантаження сторінки
        } else {
            showMessage(result.message);
        }
    });

    // Додаємо рядок
    addRowForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(addRowForm);
        const rowValues = formData.getAll('row_values[]');
        const response = await fetch(`/api/tables/${tableIndex}/rows`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ row_values: rowValues })
        });
        const result = await response.json();
        if (result.success) {
            location.reload(); // перезавантаження сторінки
        } else {
            showMessage(result.message);
        }
    });

    // Редагування клітинок
    dataTable.addEventListener('click', async (e) => {
        const target = e.target;

        // Якщо це клітинка
        if (target.tagName === 'TD' && target.classList.contains('editable')) {
            const rowIndex = target.closest('tr').dataset.rowIndex;
            const cellIndex = Array.from(target.parentNode.children).indexOf(target); // індекс клітинки

            if (!target.isContentEditable) {
                target.setAttribute('contenteditable', 'true');
                target.focus();
            }

            target.addEventListener('blur', async () => {
                target.setAttribute('contenteditable', 'false'); // вимикаємо редагування

                const newValue = target.textContent.trim();

                // Відправляємо оновлене значення на сервер
                const response = await fetch(`/api/tables/${tableIndex}/rows/${rowIndex}/cell`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        new_value: newValue,
                        col_index: cellIndex
                    })
                });

                const result = await response.json();
                if (result.success) {
                    target.style.backgroundColor = '#d4edda'; // Зелене тло після успішного оновлення
                    showMessage('Cell updated successfully');
                } else {
                    target.style.backgroundColor = '#f8d7da'; // Червоне тло у разі помилки
                    showMessage(result.message);
                }
            });
        }
    });

    // Видалення рядка
    dataTable.addEventListener('click', async (e) => {
        if (e.target.classList.contains('delete-row')) {
            const rowIndex = e.target.dataset.rowIndex;
            const confirmed = confirm('Are you sure you want to delete this row?');
            if (confirmed) {
                const response = await fetch(`/api/tables/${tableIndex}/rows/${rowIndex}`, {
                    method: 'DELETE',
                    headers: { 'Content-Type': 'application/json' }
                });
                const result = await response.json();
                if (result.success) {
                    showMessage('Row deleted successfully');
                    location.reload(); // Перезавантажуємо сторінку після видалення
                } else {
                    showMessage(result.message);
                }
            }
        }
    });

    // Видалення таблиці
    deleteTableBtn.addEventListener('click', async () => {
        if (confirm('Are you sure you want to delete this table?')) {
            const response = await fetch(`/api/tables/${tableIndex}`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            });
            const result = await response.json();
            if (result.success) {
                window.location.href = '/';
            } else {
                showMessage(result.message);
            }
        }
    });
});
