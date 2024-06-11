#!/usr/bin/python3
""" User API endpoints """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
  """Retrieves the list of all users
  ---
  responses:
    200:
      description: All users gotten successfully
  """
  all_users = storage.all(User).values()
  list_users = []
  for user in all_users:
    list_users.append(user.to_dict())
  return (jsonify(list_users)), 200

@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
  """ Gets a user by ID
  ---
  parameters:
    - name: user_id
      in: path
      type: string
      required: true
      description: The ID of the user
  responses:
    200:
      description: User information gotten successfully
    404:
      description: User not found
  """
  user = storage.get(User, user_id)
  if not user:
    abort(404)
  return jsonify(user.to_dict()), 200

@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
  """ Deletes a user object
  ---
  parameters:
    - name: user_id
      in: path
      type: string
      required: true
      description: The ID of the user
  responses:
    204:
      description: User deleted successfully
    404:
      description: User not found
  """
  user = storage.get(User, user_id)
  if not user:
    abort(404)
  
  user.delete()
  storage.save()
  return make_response(jsonify({}), 204)

@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
  """ Creates a user
  ---
  parameters:
      - name: user_and_password
        in: body
        required: true
        requires:
          - email:
          - first_name:
          - last_name
        properties:
          email:
            type: string
          first_name:
            type: string
          last_name:
            type: string
  responses:
    201:
      description: User created successfully
    400:
      description: Invalid JSON or missing parameters
  """
  if not request.get_json():
    abort(400, description="Invalid JSON")
  
  if 'email' not in request.get_json():
    abort(400, description="Missing email")
  if 'first_name' not in request.get_json():
    abort(400, description="Missing first name")
  if 'last_name' not in request.get_json():
    abort(400, description="Missing last name")

  request_data = request.get_json()
  new_user = User(**request_data)
  new_user.save()
  return make_response(jsonify(new_user.to_dict()), 201)

@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
  """ Updates a user
  ---
  parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: The ID of the user
      - name: user_and_password
        in: body
        required: true
        requires:
          - email:
          - first_name:
          - last_name
        properties:
          email:
            type: string
          first_name:
            type: string
          last_name:
            type: string
  requestBody:
    required: true
    content:
      application/json:
        schema:
          type: object
          properties:
            email:
              type: string
              description: The email for the user
            first_name:
              type: string
              description: The first name of the user
            last_name:
              type: string
              description: The last name of the user
  responses:
    201:
      description: User updated successfully
    400:
      description: Invalid JSON or missing parameters
  """
  user = storage.get(User, user_id)
  if not user:
    abort(404)
  if not request.get_json():
    abort(400, description="Invalid JSON")
  
  ignore = ['id', 'email', 'created_at', 'updated_at']

  data = request.get_json()
  for key, value in data.items():
    if key not in ignore:
      setattr(user, key, value)
  user.save()
  return make_response(jsonify(user.to_dict()), 201)
