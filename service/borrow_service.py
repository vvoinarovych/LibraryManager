from threading import Lock
from model.waitlistQueue import WaitlistQueue
from model.historyStack import HistoryStack
from database.database import db, Book, User, BorrowRecord
from datetime import date

shared_resource_lock = Lock()

waitlist = {}
history_stack = HistoryStack()


def add_book_to_catalog(title, author, published_date=None):
    # Dodaje książkę do katalogu. Zabezpiecza dostęp do wspólnego zasobu.
    with shared_resource_lock:
        # Tworzenie obiektu książki i dodanie go do bazy danych
        book = Book(title=title, author=author, published_date=published_date, available=True)
        db.session.add(book)
        db.session.commit()
        # Zapisanie operacji dodania książki do historii
        history_stack.push(("add book", title, author, book.id))
        return f"Book '{title}' added to catalog with ID {book.id}."


def find_book_in_catalog(book_id):
    # Znajduje książkę w katalogu na podstawie ID
    book = Book.query.get(book_id)
    if book:
        # Zwraca istotne informacje o książce
        return {
            "book_id": book.id,
            "title": book.title,
            "available": book.available
        }
    return None


def borrow_book(user_id, book_id):
    # Wypożycza książkę użytkownikowi lub dodaje go do listy oczekujących, jeśli książka jest niedostępna
    with shared_resource_lock:
        user = User.query.get(user_id)
        book = Book.query.get(book_id)

        if user and book:
            # Sprawdza, czy użytkownik już wypożyczył książkę
            active_borrow = BorrowRecord.query.filter_by(user_id=user_id, book_id=book_id, return_date=None).first()
            if active_borrow:
                return f"User {user_id} already has the book '{book.title}' borrowed."

            # Sprawdza, czy użytkownik jest już na liście oczekujących
            if book_id in waitlist and user_id in waitlist[book_id].queue:
                return f"User {user_id} is already in the waitlist for the book '{book.title}'."

            # Jeśli książka jest dostępna, wypożycza ją użytkownikowi
            if book.available:
                book.available = False  # Zmiana stanu książki na niedostępną
                db.session.add(BorrowRecord(user_id=user_id, book_id=book_id, borrow_date=date.today()))
                db.session.commit()
                # Zapisanie operacji wypożyczenia książki do historii
                history_stack.push(("borrow book", user_id, book_id))
                return f"Book '{book.title}' borrowed successfully!"
            else:
                # Jeśli książka jest niedostępna, dodaje użytkownika do listy oczekujących
                if book_id not in waitlist:
                    waitlist[book_id] = WaitlistQueue()  # Tworzy nową kolejkę dla książki
                waitlist[book_id].enqueue(user_id)
                print(f"User {user_id} added to the waitlist for book {book_id}.")
                # Zapisanie operacji dodania użytkownika do listy oczekujących w historii
                history_stack.push(("add user to waitlist", user_id, book_id))
                return f"Book '{book.title}' is not available. User {user_id} added to the waitlist."

        return "User or book not found."


def return_book(book_id):
    # Zwraca książkę i przypisuje ją następnemu użytkownikowi z listy oczekujących, jeśli taka istnieje
    with shared_resource_lock:
        borrow = BorrowRecord.query.filter_by(book_id=book_id).filter_by(return_date=None).first()
        book = Book.query.get(book_id)

        if book and borrow:
            borrow.return_date = date.today()  # Ustawienie daty zwrotu książki

            # Jeśli jest lista oczekujących, przypisuje książkę następnemu użytkownikowi
            if book_id in waitlist and not waitlist[book_id].is_empty():
                next_user_id = waitlist[book_id].dequeue()  # Pobranie użytkownika z kolejki
                db.session.add(BorrowRecord(user_id=next_user_id, book_id=book_id, borrow_date=date.today()))
                db.session.commit()
                # Zapisanie operacji zwrotu książki i przypisania jej użytkownikowi z listy oczekujących
                history_stack.push(("return book and assign to waitlist user", borrow.user_id, book_id, next_user_id))
                return f"Book '{book.title}' returned and borrowed by user {next_user_id} from the waitlist."
            else:
                # Jeśli nikt nie czeka, książka staje się dostępna
                book.available = True
                db.session.commit()
                # Zapisanie operacji zwrotu książki do historii
                history_stack.push(("return book", borrow.user_id, book_id))
                return f"Book '{book.title}' returned successfully and is now available."

        return "No active borrow record found for this book."


def list_all_books():
    # Zwraca listę wszystkich książek w katalogu
    with shared_resource_lock:
        books = Book.query.all()
        book_list = []
        for book in books:
            # Tworzenie słownika z istotnymi danymi o książce
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
    # Zwraca wszystkie operacje z historii w odwróconej kolejności
    with shared_resource_lock:
        reversed_operations = []
        temp_stack = history_stack.stack.copy()  # Tworzy kopię historii
        while temp_stack:
            # Usuwanie i dodawanie operacji z kopii stosu
            operation = temp_stack.pop()
            reversed_operations.append(operation)
        return reversed_operations
