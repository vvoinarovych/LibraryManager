document.addEventListener('DOMContentLoaded', () => {
    const addUserForm = document.getElementById('add-user-form');
    const usersTable = document.getElementById('users-table').querySelector('tbody');

    fetchUsers();

    addUserForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        console.log(1)

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;

        try {
            console.log("test")
            const response = await fetch('/users/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({name, email})
            });

            const data = await response.json();
            alert(data.message || data.error);
            if (response.ok) {
                addUserForm.reset();
                fetchUsers();
            }
        } catch (error) {
            console.error('Error adding user:', error);
            alert('Error adding user.');
        }
    });

    async function fetchUsers() {
        try {
            console.log(2)
            const response = await fetch('/users/list');
            if (response.ok) {
                const data = await response.json();
                usersTable.innerHTML = '';
                if (data.users && data.users.length) {
                    data.users.forEach((user) => {
                        const row = `<tr>
                        <td>${user.id}</td>
                        <td>${user.name}</td>
                        <td>${user.email}</td>
                        <td>
                            <button class="delete-user-btn" data-user-id="${user.id}">Delete</button>
                        </td>
                    </tr>`;
                        usersTable.innerHTML += row;
                    });
                } else {
                    usersTable.innerHTML = '<tr><td colspan="4">No users found.</td></tr>';
                }
                attachDeleteButtons();
            } else {
                usersTable.innerHTML = '<tr><td colspan="4">Failed to load users.</td></tr>';
            }
        } catch (error) {
            console.error('Error fetching users:', error);
            usersTable.innerHTML = '<tr><td colspan="4">Error loading users.</td></tr>';
        }
    }


    function attachDeleteButtons() {
        document.querySelectorAll('.delete-user-btn').forEach((button) => {
            button.addEventListener('click', async (event) => {
                const userId = event.target.getAttribute('data-user-id');
                if (confirm(`Are you sure you want to delete user ID ${userId}?`)) {
                    try {
                        const response = await fetch(`/users/${userId}`, {
                            method: 'DELETE',
                        });

                        const data = await response.json();
                        alert(data.message || data.error);
                        if (response.ok) {
                            fetchUsers();
                        }
                    } catch (error) {
                        console.error('Error deleting user:', error);
                        alert('Error deleting user.');
                    }
                }
            });
        });
    }
});
