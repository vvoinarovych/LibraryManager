from threading import Lock
from database.database import User, db

shared_resource_lock = Lock()

def create_user(name, email):
    if not name or not email:
        return {'error': 'Name and email are required'}

    try:
        if User.query.filter_by(email=email).first():
            return {'error': 'Email already exists'}

        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()

        return {
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        }
    finally:
        shared_resource_lock.release()

def delete_user(user_id):
    shared_resource_lock.acquire()
    try:
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}

        db.session.delete(user)
        db.session.commit()

        return {'message': 'User deleted successfully'}
    finally:
        shared_resource_lock.release()

def list_users():
    with shared_resource_lock:
        users = User.query.all()
        user_list = [
            {'id': user.id, 'name': user.name, 'email': user.email}
            for user in users
        ]
        return {'users': user_list}