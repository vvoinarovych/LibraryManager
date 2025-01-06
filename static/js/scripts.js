document.addEventListener('DOMContentLoaded', function () {
    const addBookForm = document.getElementById('add-book-form');
    const booksTable = document.getElementById('books-table').querySelector('tbody');

    fetchBooks();

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
                </tr>`;
                booksTable.innerHTML += row;
            });
        } else {
            booksTable.innerHTML = '<tr><td colspan="4">No books available.</td></tr>';
        }
    }
});
