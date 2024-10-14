document.addEventListener('DOMContentLoaded', (event) => {
    const createDbForm = document.getElementById('create-db-form');
    const addTableForm = document.getElementById('add-table-form');
    const tableList = document.getElementById('table-list');
    const saveDbButton = document.getElementById('save-db-button');
    const openDbButton = document.getElementById('open-db-button');
    const fileInput = document.getElementById('file-input');

    createDbForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const dbName = createDbForm.elements['db_name'].value;
        const response = await fetch('/api/create_db', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({db_name: dbName})
        });
        const result = await response.json();
        alert(result.message);
    });

    addTableForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const tableName = addTableForm.elements['table_name'].value;
        const response = await fetch('/api/tables', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({table_name: tableName})
        });
        const result = await response.json();
        if (result.success) {
            updateTableList();
        }
        alert(result.message);
    });

    saveDbButton.addEventListener('click', async () => {
        const filePath = prompt("Enter file name to save the database (without extension):");

        if (filePath) {
            const response = await fetch('/api/save_db', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ file_path: filePath })  // Відправляємо ім'я файлу без розширення
            });

            const result = await response.json();
            if (result.success) {
                // Створюємо посилання для збереження файлу
                const a = document.createElement('a');
                a.href = `/uploads/${result.file_path}`;  // URL для завантаження файлу з .db
                a.download = result.file_path;
                document.body.appendChild(a);
                a.click();  // відкриваємо діалогове вікно для збереження
                document.body.removeChild(a);
            } else {
                alert(result.message);
            }
        }
    });
    openDbButton.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);
            const response = await fetch('/api/open_db', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            if (result.success) {
                updateTableList();
            }
            alert(result.message);
        }
    });

    async function updateTableList() {
        const response = await fetch('/api/tables');
        const data = await response.json();
        tableList.innerHTML = '';
        data.tables.forEach((table, index) => {
            const li = document.createElement('li');
            li.innerHTML = `<a href="/table/${index}">${table}</a>`;
            tableList.appendChild(li);
        });
    }

    updateTableList();
});