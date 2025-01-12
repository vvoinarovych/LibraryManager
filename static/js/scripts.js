document.addEventListener('DOMContentLoaded', function () {
    const addBookForm = document.getElementById('add-book-form');
    const booksTable = document.getElementById('books-table').querySelector('tbody');
    const waitlistTable = document.getElementById('waitlist-table').querySelector('tbody');
    const undoStackTable = document.getElementById('undo-stack-table').querySelector('tbody');

    fetchBooks();
    fetchWaitlists();
    fetchUndoStack();

    addBookForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const title = document.getElementById('title').value;
        const author = document.getElementById('author').value;

        const response = await fetch('/books/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, author }),
        });

        const data = await response.json();
        alert(data.message);
        addBookForm.reset();
        fetchBooks();
        fetchWaitlists();
        fetchUndoStack();
    });

    async function fetchBooks() {
        const response = await fetch('/books/list');
        if (response.ok) {
            const books = await response.json();
            booksTable.innerHTML = '';
            books.forEach((book) => {
                const row = `<tr>
                    <td>${book.id}</td>
                    <td>${book.title}</td>
                    <td>${book.author}</td>
                    <td>${book.available ? 'Yes' : 'No'}</td>
                    <td>
                        <button class="borrow-btn" data-book-id="${book.id}">
                            ${book.available ? 'Borrow' : 'Join Waitlist'}
                        </button>
                    </td>
                    <td>
                        ${!book.available ? `<button class="return-btn" data-book-id="${book.id}">Return</button>` : ''}
                    </td>
                </tr>`;
                booksTable.innerHTML += row;
            });

            document.querySelectorAll('.borrow-btn').forEach(button => {
                button.addEventListener('click', async (event) => {
                    const bookId = event.target.getAttribute('data-book-id');
                    const userId = prompt('Enter your user ID:');
                    if (userId) {
                        const response = await fetch('/books/borrow', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ user_id: userId, book_id: bookId }),
                        });
                        const data = await response.json();
                        alert(data.message);
                        fetchBooks();
                        fetchWaitlists();
                        fetchUndoStack();
                    }
                });
            });

            document.querySelectorAll('.return-btn').forEach(button => {
                button.addEventListener('click', async (event) => {
                    const bookId = event.target.getAttribute('data-book-id');
                    const userId = prompt('Enter your user ID:');
                    if (userId) {
                        const response = await fetch('/books/return', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ user_id: userId, book_id: bookId }),
                        });
                        const data = await response.json();
                        alert(data.message);
                        fetchBooks();
                        fetchWaitlists();
                        fetchUndoStack();
                    }
                });
            });
        } else {
            booksTable.innerHTML = '<tr><td colspan="6">No books available.</td></tr>';
        }
    }

    async function fetchWaitlists() {
        const response = await fetch('/books/waitlist');
        if (response.ok) {
            const waitlists = await response.json();
            waitlistTable.innerHTML = '';
            if (Object.keys(waitlists).length > 0) {
                Object.entries(waitlists).forEach(([bookId, users]) => {
                    const usersList = users.map(userId => `User ${userId}`).join(', ');
                    const row = `<tr>
                        <td>${bookId}</td>
                        <td>${usersList}</td>
                    </tr>`;
                    waitlistTable.innerHTML += row;
                });
            } else {
                waitlistTable.innerHTML = '<tr><td colspan="2">No users on any waitlist.</td></tr>';
            }
        } else {
            waitlistTable.innerHTML = '<tr><td colspan="2">Failed to load waitlists.</td></tr>';
        }
    }

    async function fetchUndoStack() {
        const response = await fetch('/books/undo_stack');
        if (response.ok) {
            const data = await response.json();
            undoStackTable.innerHTML = '';
            if (data.undo_stack && data.undo_stack.length > 0) {
                data.undo_stack.forEach(action => {
                    const row = `<tr><td>${action[0]}</td><td>User ${action[1]}, Book ${action[2]}</td></tr>`;
                    undoStackTable.innerHTML += row;
                });
            } else {
                undoStackTable.innerHTML = '<tr><td colspan="2">No actions in undo stack.</td></tr>';
            }
        } else {
            undoStackTable.innerHTML = '<tr><td colspan="2">Failed to load undo stack.</td></tr>';
        }
    }
});
