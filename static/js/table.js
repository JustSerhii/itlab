document.addEventListener('DOMContentLoaded', (event) => {
    const addColumnForm = document.getElementById('add-column-form');
    const addRowForm = document.getElementById('add-row-form');
    const dataTable = document.getElementById('data-table');
    const deleteTableBtn = document.getElementById('delete-table-btn');
    const tableIndex = addColumnForm.elements['table_index'].value;
    const messageBox = document.createElement('div');

    // Add a message box for success or error messages
    document.body.appendChild(messageBox);
    messageBox.style.position = 'fixed';
    messageBox.style.top = '10px';
    messageBox.style.right = '10px';
    messageBox.style.padding = '10px';
    messageBox.style.backgroundColor = '#4caf50';
    messageBox.style.color = '#fff';
    messageBox.style.display = 'none';

    function showMessage(message, isError = false) {
        messageBox.textContent = message;
        messageBox.style.backgroundColor = isError ? '#f44336' : '#4caf50';  // Red for errors, green for success
        messageBox.style.display = 'block';
        setTimeout(() => {
            messageBox.style.display = 'none';
        }, 2000);
    }

    // Add column
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
            location.reload(); // reload the page
        } else {
            showMessage(result.message, true); // show error message
        }
    });

    // Add row
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
            location.reload(); // reload the page if row was added successfully
        } else {
            showMessage(result.message, true); // show error message, e.g. "Duplicate ID"
        }
    });

    // Edit cells
    dataTable.addEventListener('click', async (e) => {
        const target = e.target;

        // If it's a table cell (TD)
        if (target.tagName === 'TD' && target.classList.contains('editable')) {
            const rowIndex = target.closest('tr').dataset.rowIndex;
            const cellIndex = Array.from(target.parentNode.children).indexOf(target); // get cell index

            if (!target.isContentEditable) {
                target.setAttribute('contenteditable', 'true');
                target.focus();
            }

            target.addEventListener('blur', async () => {
                target.setAttribute('contenteditable', 'false'); // disable editing after blur

                const newValue = target.textContent.trim();

                // Send updated value to the server for validation and update
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
                    target.style.backgroundColor = '#d4edda'; // Green background on success
                    showMessage('Cell updated successfully');
                } else {
                    target.style.backgroundColor = '#f8d7da'; // Red background on error
                    showMessage(result.message, true); // show error message
                }
            });
        }
    });

    // Delete row
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
                    location.reload(); // Reload the page after deletion
                } else {
                    showMessage(result.message, true);
                }
            }
        }
    });

    // Delete table
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
                showMessage(result.message, true);
            }
        }
    });
});
