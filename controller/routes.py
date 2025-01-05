from flask import Blueprint, jsonify, request

from database.database import Book
from service.borrowService import borrow_book, return_book, add_book_to_catalog, list_all_books

routes = Blueprint('routes', __name__)

@routes.route('/books/borrow', methods=['POST'])
def borrow():
    data = request.json
    return jsonify({"message": borrow_book(data['user_id'], data['book_id'])})

@routes.route('/books/return', methods=['POST'])
def return_borrowed_book():
    data = request.json
    print(data)
    return jsonify({"message": return_book(data['user_id'], data['book_id'])})

@routes.route('/books', methods=['GET'])
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


