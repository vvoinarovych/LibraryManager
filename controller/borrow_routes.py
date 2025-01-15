from flask import Blueprint, jsonify, request, render_template
import asyncio
from service.borrow_service import borrow_book, return_book, add_book_to_catalog, waitlist, \
    get_all_reversed_history_operations, list_all_books
from utils.sorting import quicksort

borrow_routes = Blueprint('borrow_routes', __name__)


@borrow_routes.route('/')
def home():
    return render_template('index.html')


@borrow_routes.route('/books')
def books():
    return render_template('books.html')


@borrow_routes.route('/books/borrow', methods=['POST'])
async def borrow():
    data = request.get_json()
    result = await asyncio.to_thread(borrow_book, data['user_id'], data['book_id'])
    return jsonify({"message": result})


@borrow_routes.route('/books/return', methods=['POST'])
async def return_borrowed_book():
    data = request.get_json()
    result = await asyncio.to_thread(return_book, data['book_id'])
    return jsonify({"message": result})


@borrow_routes.route('/books/list', methods=['GET'])
async def get_books():
    sort_by = request.args.get('sort_by', default=None, type=str)
    books = await asyncio.to_thread(list_all_books)

    if not books:
        return jsonify({"message": "No books found."}), 404

    if sort_by == 'title':
        books = quicksort(books, key_func=lambda x: x['title'].lower())
    elif sort_by == 'author':
        books = quicksort(books, key_func=lambda x: x['author'].lower())

    return jsonify(books)


@borrow_routes.route('/books/add', methods=['POST'])
async def add_book():
    data = request.get_json()
    if 'title' in data and 'author' in data:
        result = await asyncio.to_thread(add_book_to_catalog, data['title'], data['author'], data.get('published_date'))
        return jsonify({"message": result})
    return jsonify({"error": "Invalid data"}), 400


@borrow_routes.route('/books/waitlist', methods=['GET'])
async def get_all_waitlists():
    try:
        all_waitlists = await asyncio.to_thread(lambda: {key: queue.get_all_for_display() for key, queue in waitlist.items()})
    except Exception as e:
        print(f"Error processing waitlist: {e}")
        return jsonify({"error": "Failed to process waitlist data"}), 500
    return jsonify(all_waitlists)


@borrow_routes.route('/books/history', methods=['GET'])
async def get_undo_stack():
    undo_data = await asyncio.to_thread(get_all_reversed_history_operations)
    return jsonify({"undo_stack": undo_data})
