#!/usr/bin/python3
""" User API endpoints """
import requests.adapters
from models.user import User
from models import storage
import requests
import json
from redis import StrictRedis
from datetime import timedelta
from api.v1.views import app_views
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from flask import abort, jsonify, make_response, current_app, request

jwt_redis_blocklist = StrictRedis(
     host="localhost", port=6379, db=0, decode_responses=True
  )

@app_views.route('/users', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_users():
  """Retrieves the list of all users
  ---
  parameters:
    - name: Authorization
      in: header
      required: true
      description: Bearer <access token>
      type: string
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
@jwt_required()
def get_user(user_id):
  """ Gets a user by ID
  ---
  parameters:
    - name: Authorization
      in: header
      required: true
      description: Bearer <access token>
      type: string
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
@jwt_required()
def delete_user(user_id):
  """ Deletes a user object
  ---
  parameters:
    - name: Authorization
      in: header
      required: true
      description: Bearer <access token>
      type: string
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
  current_app.logger.critical(f"User {user_id} has been deleted")
  return make_response(jsonify({}), 204)

@app_views.route('/users/login', methods=['POST'],
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

  try:
    response_from_ad_service = requests.post(
      'https://adservice.abujaelectricity.com/auth/detail',
      request_data
    )
    current_app.logger.critical("User successfully authenticated")
  except Exception as e:
    current_app.logger.critical(f"AD service not available due to error {e}")
    abort(404)
  response = response_from_ad_service.json()
  print(response)
  if (response['status_code'] == '404'):
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
    user = storage.get_user_by_email(response_data['mail'])
    if (user):
      user_response = user.make_user_response()
      current_app.logger.critical("Existing user has logged in")
      access_token = create_access_token(identity=user_response['id'])
      return make_response(jsonify(user=user_response, token=access_token), 200)
    else:
      try:
        new_user = User(**user_object)
      except requests.exceptions.HTTPError as err:
          current_app.logger.critical(
            f"New user could not be created due to error: {err.response.status_code} {err.response}"
          )
          abort(err.response.status_code, description=err.response)
      finally:
        new_user.save()
        user_response = new_user.make_user_response()
        current_app.logger.critical("New user has been created and logged in")
        access_token = create_access_token(identity=user_response['id'])
        return make_response(jsonify(user=user_response, token=access_token), 200)
  else:
    abort(response['status_code'], description=response['msg'])

@app_views.route('/users/logout', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def logout():
  """Logs out a user
  ---
  parameters:
    - name: Authorization
      in: header
      required: true
      description: Bearer <access token>
      type: string
  responses:
    200:
      description: User access revoked
    500:
      description: Internal server error
  """
  jti = get_jwt()["jti"]
  try:
    jwt_redis_blocklist.set(jti, "", ex=timedelta(hours=1))
  except Exception as e:
    current_app.logger.critical(f"Logout failed due to exception {e}")
    abort(500, description="Internal server error")
  return jsonify(msg="Access token revoked")

@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
@jwt_required()
def update_user(user_id=None):
  """ Updates a user
  ---
  parameters:
      - name: Authorization
        in: header
        required: true
        description: Bearer <access token>
        type: string
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
  if not request.get_json():
    abort(400, description="Invalid JSON") 
  user = storage.get(User, user_id)
  if not user:
    abort(404)
  
  ignore = ['id', 'email', 'created_at', 'updated_at']

  data = request.get_json()
  for key, value in data.items():
    if key not in ignore:
      setattr(user, key, value)
  user.save()
  current_app.logger.critical("User information has been updated")
  return make_response(jsonify(user.make_user_response()), 201)
