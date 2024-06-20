#!/usr/bin/python3
""" User API endpoints """
from models.user import User
from models import storage
import requests
import json
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
def user_auth():
  """ Authenticates a user
  ---
  parameters:
      - name: user_and_password
        in: body
        required: true
        requires:
          - username:
          - password:
        properties:
          username:
            type: string
          password:
            type: string
  responses:
    200:
      description: User authentication successful
    400:
      description: Invalid JSON or missing parameters
    404:
      description: Authentication failed
  """
  if not request.get_json():
    abort(400, description="Invalid JSON")
  
  if 'username' not in request.get_json():
    abort(400, description="Missing username")
  if 'password' not in request.get_json():
    abort(400, description="Missing password")

  request_data = request.get_json()
  response_from_ad_service = requests.post(
    'https://adservice.abujaelectricity.com/auth/detail',
    request_data
  )
  response = response_from_ad_service.json()
  print(response)
  if (response['status_code'] == '404'):
    print("GOT TO CONDITIONAL STATEMENT")
    abort(404)
  elif (response['status_code'] == '200'):
    response_data = response['data']
    print(response_data['mail'])
    print("GOT TO THE ELSE OF THE CONDITIONAL STATEMENT")
    user_object = {
      'email': response_data['mail'],
      'first_name': response_data['firstname'],
      'last_name': response_data['surname']
    }
    if (storage.get_user_by_email(response_data['mail'])):
      return make_response(jsonify(user_object), 200)
    else:
      try:
        new_user = User(**user_object)
      except requests.exceptions.HTTPError as err:
          abort(err.response.status_code, description=err.response)
      finally:
        new_user.save()
        return make_response(jsonify(user_object), 200)
  else:
    abort(response['status_code'], description=response['msg'])

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
