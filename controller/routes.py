from flask import Blueprint, jsonify, request, render_template

from database.database import Book
from service.borrowService import borrow_book, return_book, add_book_to_catalog, list_all_books, waitlist, undo_stack, \
    get_all_reversed_undo_operations

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('index.html')

@routes.route('/books')
def books():
    return render_template('books.html')


@routes.route('/books/borrow', methods=['POST'])
def borrow():
    data = request.json
    return jsonify({"message": borrow_book(data['user_id'], data['book_id'])})

@routes.route('/books/return', methods=['POST'])
def return_borrowed_book():
    data = request.json
    print(data)
    return jsonify({"message": return_book(data['user_id'], data['book_id'])})

@routes.route('/books/list', methods=['GET'])
def get_books():
    books = Book.query.all()
    if not books:
        return jsonify({"message": "No books found."}), 404

    book_list = []
    for book in books:
        book_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'published_date': book.published_date,
            'available': book.available
        }
        book_list.append(book_data)

    return jsonify(book_list)

@routes.route('/books/add', methods=['POST'])
def add_book():
    data = request.get_json()
    if 'title' in data and 'author' in data:
        message = add_book_to_catalog(data['title'], data['author'], data.get('published_date'))
        return jsonify({"message": message})
    return jsonify({"error": "Invalid data"}), 400

@routes.route('/books/list', methods=['GET'])
def list_books():
    books = list_all_books()
    return jsonify({"books": books})

@routes.route('/books/waitlist', methods=['GET'])
def get_all_waitlists():
    try:
        all_waitlists = {key: queue.get_all_for_display() for key, queue in waitlist.items()}
    except Exception as e:
        print(f"Error processing waitlist: {e}")
        return jsonify({"error": "Failed to process waitlist data"}), 500
    return jsonify(all_waitlists)

@routes.route('/books/undo_stack', methods=['GET'])
def get_undo_stack():
    undo_data = get_all_reversed_undo_operations()
    return jsonify({"undo_stack": undo_data})

