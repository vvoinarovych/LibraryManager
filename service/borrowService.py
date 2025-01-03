from model.BST import BST
from model.waitlistQueue import WaitlistQueue
from model.undoStack import UndoStack
from database.database import db, Book, User, BorrowRecord
from datetime import date

waitlist = {}
undo_stack = UndoStack()
book_catalog = BST()

def borrow_book(user_id, book_id):
    user = User.query.get(user_id)
    book = Book.query.get(book_id)
    if user:
        if book and book.available:
            book.available = False
            db.session.add(BorrowRecord(user_id=user_id, book_id=book_id, borrow_date=date.today()))
            db.session.commit()
            undo_stack.push(("return_book", user_id, book_id))
            return f"Book {book.title} borrowed successfully!"
        elif book:
            if book_id not in waitlist:
                waitlist[book_id] = WaitlistQueue()
            waitlist[book_id].enqueue(user_id)
            return "Book not available, added to the waitlist."
    return "User or book not found."

def return_book(user_id, book_id):
    user = User.query.get(user_id)
    borrow = BorrowRecord.query.filter_by(user_id=user_id, book_id=book_id).first()
    if user and borrow:
        borrow.return_date = date.today()
        book = Book.query.get(book_id)
        book.available = True
        db.session.commit()
        undo_stack.push(("borrow_book", user_id, book_id))
        return f"Book {book.title} returned successfully!"
    return "Borrow record not found or user not found."
