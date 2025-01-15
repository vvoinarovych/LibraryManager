from flask import Blueprint, jsonify, request, render_template
import asyncio
from service.user_service import create_user, delete_user, list_users

# Blueprint to handle user-related routes
user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/users')
def users_page():
    # Route to render the users page template
    return render_template('users.html')


@user_routes.route('/users/add', methods=['POST'])
async def create_user_route():
    # Route to handle creation of a new user
    # Asynchronously calls the create_user function from the user service
    data = request.get_json()
    # Checks if the necessary fields are present in the request data
    if 'name' in data and 'email' in data:
        result = await asyncio.to_thread(create_user, data['name'], data['email'])
        # Returns the result of user creation as a JSON response
        return jsonify(result)
    # Returns an error if the required data is missing
    return jsonify({"error": "Invalid data"}), 400


@user_routes.route('/users/list', methods=['GET'])
async def list_users_route():
    # Route to fetch and list all users
    try:
        print("Fetching users")
        # Asynchronously fetches the list of users using the list_users function
        result = await asyncio.to_thread(list_users)
        if 'users' in result:
            # If users are found, return the result with a 200 status code
            return jsonify(result), 200
        else:
            print("No users found", result)
            # If no users are found, return an error message
            return jsonify({'error': 'No users found'}), 404
    except Exception as e:
        # If there is an exception during fetching users, return a 500 error message
        print("Error fetching users:", str(e))
        return jsonify({'error': 'Error fetching users: ' + str(e)}), 500


@user_routes.route('/users/<int:user_id>', methods=['DELETE'])
async def delete_user_route(user_id):
    # Route to delete a user based on their ID
    try:
        # Asynchronously calls the delete_user function to delete the user
        result = await asyncio.to_thread(delete_user, user_id)
        return jsonify(result)
    except Exception as e:
        # If there is an exception during deletion, return a 500 error message
        return jsonify({'error': str(e)}), 500
