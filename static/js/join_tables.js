document.addEventListener('DOMContentLoaded', (event) => {
    const joinTablesForm = document.getElementById('join-tables-form');
    const joinResult = document.getElementById('join-result');

    joinTablesForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(joinTablesForm);
        const data = {
            table1_index: formData.get('table1_index'),
            table2_index: formData.get('table2_index'),
            column1_name: formData.get('column1_name'),
            column2_name: formData.get('column2_name')
        };
        const response = await fetch('/api/join_tables', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (result.success) {
            displayJoinedTable(result.joined_data);
        } else {
            alert(result.message);
        }
    });

    function displayJoinedTable(data) {
        let tableHtml = '<table><thead><tr>';
        data[0].forEach(header => {
            tableHtml += `<th>${header}</th>`;
        });
        tableHtml += '</tr></thead><tbody>';
        data.slice(1).forEach(row => {
            tableHtml += '<tr>';
            row.forEach(cell => {
                tableHtml += `<td>${cell}</td>`;
            });
            tableHtml += '</tr>';
        });
        tableHtml += '</tbody></table>';
        joinResult.innerHTML = tableHtml;
    }
});