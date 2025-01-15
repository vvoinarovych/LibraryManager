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
            active_borrow = BorrowRecord.query.filter_by(user_id=user_id, book_id=book_id, return_date=None).first()
            if active_borrow:
                return f"User {user_id} already has the book '{book.title}' borrowed."

            if book_id in waitlist and user_id in waitlist[book_id].queue:
                return f"User {user_id} is already in the waitlist for the book '{book.title}'."

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
                return f"Book '{book.title}' is not available. User {user_id} added to the waitlist."

        return "User or book not found."


def return_book(book_id):
    with shared_resource_lock:
        borrow = BorrowRecord.query.filter_by(book_id=book_id).filter_by(return_date=None).first()
        book = Book.query.get(book_id)

        if book and borrow:
            borrow.return_date = date.today()

            if book_id in waitlist and not waitlist[book_id].is_empty():
                next_user_id = waitlist[book_id].dequeue()

                db.session.add(BorrowRecord(user_id=next_user_id, book_id=book_id, borrow_date=date.today()))
                db.session.commit()

                history_stack.push(("return book and assign to waitlist user", borrow.user_id, book_id, next_user_id))
                return f"Book '{book.title}' returned and borrowed by user {next_user_id} from the waitlist."
            else:
                book.available = True
                db.session.commit()
                history_stack.push(("return book", borrow.user_id, book_id))
                return f"Book '{book.title}' returned successfully and is now available."

        return "No active borrow record found for this book."


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
