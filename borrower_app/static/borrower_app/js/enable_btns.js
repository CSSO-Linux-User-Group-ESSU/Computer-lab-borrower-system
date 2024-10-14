const modifyButton = document.getElementById('modify-button');
const deleteButton = document.getElementById('delete-button');
const checkboxes = document.querySelectorAll('.select-borrower');

checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        const anyChecked = [...checkboxes].some(cb => cb.checked);
        modifyButton.disabled = !anyChecked;  // Disable if none checked
        deleteButton.disabled = !anyChecked;  // Disable if none checked
    });
});

modifyButton.addEventListener('click', () => {
    // Gather selected borrower IDs
    const selectedIds = [...checkboxes].filter(cb => cb.checked).map(cb => cb.value);

    if (selectedIds.length === 1) {
        // Redirect to modify page with selected ID
        window.location.href = "{% url 'modify_borrower' 0 %}".replace("0", selectedIds[0]);
    } else {
        alert("Please select exactly one borrower to modify.");
    }
});

deleteButton.addEventListener('click', () => {
    const selectedIds = [...checkboxes].filter(cb => cb.checked).map(cb => cb.value);

    if (selectedIds.length > 0) {
        if (confirm('Are you sure you want to delete the selected borrowers?')) {
            fetch("{% url 'delete_borrowers' %}", {
                method: "POST",
                headers: {
                    "X-CSRFToken": "{{ csrf_token }}",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ borrower_ids: selectedIds })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload(); // Reload the page after successful deletion
                } else {
                    alert("An error occurred while deleting borrowers.");
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("An error occurred. Please try again later.");
            });
        }
    }
});