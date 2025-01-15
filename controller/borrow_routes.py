from flask import Blueprint, jsonify, request, render_template
import asyncio
from service.borrow_service import borrow_book, return_book, add_book_to_catalog, waitlist, \
    get_all_reversed_history_operations, list_all_books
from utils.sorting import quicksort

borrow_routes = Blueprint('borrow_routes', __name__)


@borrow_routes.route('/')
def home():
    # Wyświetla stronę główną (index.html)
    return render_template('index.html')


@borrow_routes.route('/books')
def books():
    # Wyświetla stronę, gdzie można przeglądać książki (books.html)
    return render_template('books.html')


@borrow_routes.route('/books/borrow', methods=['POST'])
async def borrow():
    # Endpoint umożliwiający wypożyczenie książki
    # Oczekuje danych w formacie JSON (user_id, book_id)
    data = request.get_json()

    # Wykonanie funkcji borrow_book w wątku roboczym asynchronicznie, aby nie blokować głównego wątku
    result = await asyncio.to_thread(borrow_book, data['user_id'], data['book_id'])

    # Zwraca odpowiedź z komunikatem, czy operacja wypożyczenia książki powiodła się
    return jsonify({"message": result})


@borrow_routes.route('/books/return', methods=['POST'])
async def return_borrowed_book():
    # Endpoint umożliwiający zwrot książki
    # Oczekuje danych w formacie JSON (book_id)
    data = request.get_json()

    # Wykonanie funkcji return_book w wątku roboczym asynchronicznie
    result = await asyncio.to_thread(return_book, data['book_id'])

    # Zwraca odpowiedź z komunikatem o wyniku zwrotu książki
    return jsonify({"message": result})


@borrow_routes.route('/books/list', methods=['GET'])
async def get_books():
    # Endpoint do pobierania listy książek. Może opcjonalnie sortować według tytułu lub autora
    sort_by = request.args.get('sort_by', default=None, type=str)

    # Pobieranie wszystkich książek w wątku roboczym
    books = await asyncio.to_thread(list_all_books)

    if not books:
        return jsonify({"message": "No books found."}), 404  # Jeśli brak książek w katalogu, zwraca błąd

    # Sortowanie książek, jeśli parametr sort_by jest określony
    if sort_by == 'title':
        books = quicksort(books, key_func=lambda x: x['title'].lower())  # Sortowanie po tytule
    elif sort_by == 'author':
        books = quicksort(books, key_func=lambda x: x['author'].lower())  # Sortowanie po autorze

    # Zwraca listę książek w formacie JSON
    return jsonify(books)


@borrow_routes.route('/books/add', methods=['POST'])
async def add_book():
    # Endpoint do dodawania książki do katalogu
    # Oczekuje danych w formacie JSON (title, author, optional published_date)
    data = request.get_json()

    # Sprawdza, czy dane zawierają tytuł i autora książki
    if 'title' in data and 'author' in data:
        # Wykonanie funkcji add_book_to_catalog w wątku roboczym
        result = await asyncio.to_thread(add_book_to_catalog, data['title'], data['author'], data.get('published_date'))
        # Zwraca komunikat o wyniku dodania książki
        return jsonify({"message": result})

    # Jeśli dane są niekompletne, zwraca błąd
    return jsonify({"error": "Invalid data"}), 400


@borrow_routes.route('/books/waitlist', methods=['GET'])
async def get_all_waitlists():
    # Endpoint do pobierania wszystkich list oczekujących
    try:
        # Wykonanie funkcji pobierania danych z listy oczekujących w wątku roboczym
        all_waitlists = await asyncio.to_thread(
            lambda: {key: queue.get_all_for_display() for key, queue in waitlist.items()})
    except Exception as e:
        # Obsługuje ewentualne błędy podczas przetwarzania danych
        print(f"Error processing waitlist: {e}")
        return jsonify({"error": "Failed to process waitlist data"}), 500

    # Zwraca dane o wszystkich listach oczekujących
    return jsonify(all_waitlists)


@borrow_routes.route('/books/history', methods=['GET'])
async def get_undo_stack():
    # Endpoint do pobierania odwróconej historii operacji (undo stack)
    # Wykonanie funkcji get_all_reversed_history_operations w wątku roboczym
    undo_data = await asyncio.to_thread(get_all_reversed_history_operations)

    # Zwraca dane o historii operacji w formacie JSON
    return jsonify({"undo_stack": undo_data})
