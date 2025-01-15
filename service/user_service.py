from threading import Lock
from database.database import User, db, BorrowRecord
from service.borrow_service import waitlist

shared_resource_lock = Lock()

def create_user(name, email):
    # Funkcja do tworzenia nowego użytkownika w systemie
    # Sprawdza, czy imię i email zostały dostarczone
    if not name or not email:
        return {'error': 'Name and email are required'}

    shared_resource_lock.acquire()  # Acquire the lock here to prevent race conditions

    try:
        # Sprawdza, czy użytkownik o podanym emailu już istnieje w systemie
        if User.query.filter_by(email=email).first():
            return {'error': 'Email already exists'}

        # Tworzy nowego użytkownika i dodaje go do bazy danych
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()

        # Zwraca dane o nowo utworzonym użytkowniku
        return {
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        }
    finally:
        # Upewnia się, że blokada zostanie zwolniona po zakończeniu operacji
        shared_resource_lock.release()  # Release the lock here

def delete_user(user_id):
    # Funkcja do usuwania użytkownika z systemu
    shared_resource_lock.acquire()  # Acquire the lock here to prevent race conditions
    try:
        # Pobiera użytkownika na podstawie jego ID
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}

        # Sprawdza, czy użytkownik ma aktywne wypożyczenia książek
        active_borrows = BorrowRecord.query.filter_by(
            user_id=user_id, return_date=None).all()
        if active_borrows:
            return {'error': 'User has active borrowed books and cannot be deleted.'}

        # Sprawdza, czy użytkownik znajduje się na liście oczekujących na książki
        in_waitlist = any(
            user_id in waitlist_queue.queue for waitlist_queue in waitlist.values())
        if in_waitlist:
            return {'error': 'User is in a waitlist and cannot be deleted.'}

        # Usuwa użytkownika z bazy danych
        db.session.delete(user)
        db.session.commit()

        return {'message': 'User deleted successfully'}
    finally:
        # Zwolnienie blokady po zakończeniu operacji
        shared_resource_lock.release()  # Release the lock here

def list_users():
    # Funkcja do pobierania listy wszystkich użytkowników
    with shared_resource_lock:
        # Pobieranie wszystkich użytkowników z bazy danych
        users = User.query.all()
        # Tworzenie listy słowników zawierających dane o użytkownikach
        user_list = [
            {'id': user.id, 'name': user.name, 'email': user.email}
            for user in users
        ]
        return {'users': user_list}
