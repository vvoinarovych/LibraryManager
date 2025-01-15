from sqlalchemy import inspect
from flask import Flask
from database.database import db
from database.config import SQLALCHEMY_DATABASE_URI
from controller.routes import routes
from database.database import Book, User, BorrowRecord
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.register_blueprint(routes)


def init_db():
    with app.app_context():
        print("Starting to initialize the database...")
        db.drop_all()
        db.create_all()

        inspector = inspect(db.engine)
        if 'books' in inspector.get_table_names():
            print("Table 'books' exists.")
        else:
            print("Table 'books' does not exist.")

        user1 = User(name='Jan Kowalski', email='jan.kowalski@example.com')
        user2 = User(name='Maria Nowak', email='maria.nowak@example.com')
        user3 = User(name='Piotr Wiśniewski',
                     email='piotr.wisniewski@example.com')

        db.session.add_all([user1, user2, user3])
        db.session.commit()

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

        db.session.add_all([book1, book2, book3, book4, book5])
        db.session.commit()

        borrow_record1 = BorrowRecord(
            user_id=1, book_id=1, borrow_date=date(2025, 1, 4), return_date=None)
        borrow_record2 = BorrowRecord(
            user_id=2, book_id=2, borrow_date=date(2025, 1, 4), return_date=None)
        borrow_record3 = BorrowRecord(
            user_id=3, book_id=3, borrow_date=date(2025, 1, 4), return_date=None)

        db.session.add_all([borrow_record1, borrow_record2, borrow_record3])
        db.session.commit()

        print("Test data has been added.")


if __name__ == '__main__':
    print("Starting the Flask application...")
    init_db()
    app.run(debug=True)
