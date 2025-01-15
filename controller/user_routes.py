from flask import Blueprint, jsonify, request, render_template
import asyncio
from service.user_service import create_user, delete_user, list_users

user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/users')
def users_page():
    return render_template('users.html')


@user_routes.route('/users/add', methods=['POST'])
async def create_user_route():
    data = request.get_json()
    if 'name' in data and 'email' in data:
        result = await asyncio.to_thread(create_user, data['name'], data['email'])
        return jsonify(result)
    return jsonify({"error": "Invalid data"}), 400


@user_routes.route('/users/list', methods=['GET'])
async def list_users_route():
    try:
        print("users")
        result = await asyncio.to_thread(list_users)
        if 'users' in result:
            return jsonify(result), 200
        else:
            print("No users found", result)
            return jsonify({'error': 'No users found'}), 404
    except Exception as e:
        print("Error fetching users:", str(e))
        return jsonify({'error': 'Error fetching users: ' + str(e)}), 500


@user_routes.route('/users/<int:user_id>', methods=['DELETE'])
async def delete_user_route(user_id):
    try:
        result = await asyncio.to_thread(delete_user, user_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
