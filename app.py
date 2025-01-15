from sqlalchemy import inspect
from flask import Flask

# Importowanie tras i modeli bazy danych
from controller.user_routes import user_routes
from database.database import db
from database.config import SQLALCHEMY_DATABASE_URI
from controller.borrow_routes import borrow_routes
from database.database import Book, User, BorrowRecord
from datetime import date

# Inicjalizacja aplikacji Flask
app = Flask(__name__)

# Konfiguracja aplikacji Flask z URI bazy danych i ustawieniami
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI  # Łącze do bazy danych
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Wyłączenie śledzenia modyfikacji w celu poprawy wydajności

# Inicjalizacja obiektu SQLAlchemy
db.init_app(app)

# Rejestrowanie blueprintów (tras)
app.register_blueprint(borrow_routes)  # Trasy związane z wypożyczeniami
app.register_blueprint(user_routes)  # Trasy związane z użytkownikami


def init_db():
    """
    Funkcja inicjalizuje bazę danych, wykonując następujące operacje:
    1. Usuwa istniejące tabele i tworzy nowe.
    2. Sprawdza, czy tabela 'books' istnieje.
    3. Dodaje przykładowe dane (użytkownicy, książki i rekordy wypożyczeń).
    """
    with app.app_context():
        print("Rozpoczynanie inicjalizacji bazy danych...")

        # Usuwanie wszystkich istniejących tabel i tworzenie nowych (resetowanie bazy danych)
        db.drop_all()
        db.create_all()

        # Inspekcja bazy danych, aby sprawdzić, czy tabela 'books' istnieje
        inspector = inspect(db.engine)
        if 'books' in inspector.get_table_names():
            print("Tabela 'books' istnieje.")
        else:
            print("Tabela 'books' nie istnieje.")

        # Tworzenie przykładowych użytkowników
        user1 = User(name='Jan Kowalski', email='jan.kowalski@example.com')
        user2 = User(name='Maria Nowak', email='maria.nowak@example.com')
        user3 = User(name='Piotr Wiśniewski', email='piotr.wisniewski@example.com')

        # Dodanie użytkowników do sesji i zapisanie ich w bazie danych
        db.session.add_all([user1, user2, user3])
        db.session.commit()

        # Tworzenie przykładowych książek z różnym statusem dostępności
        book1 = Book(title='Programowanie w Pythonie dla opornych',
                     author='Jan Kowalski', published_date=date(2022, 5, 10), available=False)
        book2 = Book(title='Flask w 24 godziny: Przewodnik po kawie',
                     author='Maria Nowak', published_date=date(2021, 8, 15), available=False)
        book3 = Book(title='Jak zostać mistrzem w PHP', author='Zbigniew Lis',
                     published_date=date(2019, 12, 1), available=False)
        book4 = Book(title='Czysty kod: Bajka o programowaniu',
                     author='Jan Kowalski', published_date=date(2020, 2, 20), available=True)
        book5 = Book(title='Historia nieudanych start-upów', author='Maria Nowak',
                     published_date=date(2023, 3, 18), available=True)

        # Dodanie książek do sesji i zapisanie ich w bazie danych
        db.session.add_all([book1, book2, book3, book4, book5])
        db.session.commit()

        # Tworzenie rekordów wypożyczeń, aby zasymulować wypożyczenia przez użytkowników
        borrow_record1 = BorrowRecord(
            user_id=1, book_id=1, borrow_date=date(2025, 1, 4), return_date=None)
        borrow_record2 = BorrowRecord(
            user_id=2, book_id=2, borrow_date=date(2025, 1, 4), return_date=None)
        borrow_record3 = BorrowRecord(
            user_id=3, book_id=3, borrow_date=date(2025, 1, 4), return_date=None)

        # Dodanie rekordów wypożyczeń do sesji i zapisanie ich
        db.session.add_all([borrow_record1, borrow_record2, borrow_record3])
        db.session.commit()

        # Informacja o zakończeniu dodawania danych testowych
        print("Dane testowe zostały dodane.")


if __name__ == '__main__':
    """
    Sekcja uruchamiająca aplikację Flask oraz inicjalizującą bazę danych.
    """
    print("Rozpoczynanie aplikacji Flask...")

    # Inicjalizacja bazy danych danymi testowymi
    init_db()

    # Uruchomienie aplikacji Flask w trybie debugowania
    app.run(debug=True)
