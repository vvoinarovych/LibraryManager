from threading import Lock
from model.waitlistQueue import WaitlistQueue
from model.historyStack import HistoryStack
from database.database import db, Book, User, BorrowRecord
from datetime import date

shared_resource_lock = Lock()

waitlist = {}
history_stack = HistoryStack()


def add_book_to_catalog(title, author, published_date=None):
    with shared_resource_lock:
        book = Book(title=title, author=author, published_date=published_date, available=True)
        db.session.add(book)
        db.session.commit()
        history_stack.push(("add book", title, author, book.id))
        return f"Book '{title}' added to catalog with ID {book.id}."


def find_book_in_catalog(book_id):
    book = Book.query.get(book_id)
    if book:
        return {
            "book_id": book.id,
            "title": book.title,
            "available": book.available
        }
    return None


def borrow_book(user_id, book_id):
    with shared_resource_lock:
        user = User.query.get(user_id)
        book = Book.query.get(book_id)

        if user and book:
            if book.available:
                book.available = False
                db.session.add(BorrowRecord(user_id=user_id, book_id=book_id, borrow_date=date.today()))
                db.session.commit()
                history_stack.push(("borrow book", user_id, book_id))
                return f"Book '{book.title}' borrowed successfully!"
            else:
                if book_id not in waitlist:
                    waitlist[book_id] = WaitlistQueue()

                waitlist[book_id].enqueue(user_id)
                print(f"User {user_id} added to the waitlist for book {book_id}.")
                history_stack.push(("add user to waitlist", user_id, book_id))
                return "Book not available, added to the waitlist."
        return "User or book not found."


def return_book(user_id, book_id):
    with shared_resource_lock:
        user = User.query.get(user_id)
        borrow = BorrowRecord.query.filter_by(user_id=user_id, book_id=book_id).first()
        book = Book.query.get(book_id)

        if user and borrow and book:
            borrow.return_date = date.today()
            book.available = True
            db.session.commit()
            history_stack.push(("return book", user_id, book_id))
            return f"Book '{book.title}' returned successfully!"
        return "Borrow record not found or user not found."


def list_all_books():
    with shared_resource_lock:
        books = Book.query.all()
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
        return book_list


def get_all_reversed_history_operations():
    with shared_resource_lock:
        reversed_operations = []
        temp_stack = history_stack.stack.copy()
        while temp_stack:
            operation = temp_stack.pop()
            reversed_operations.append(operation)
        return reversed_operations
