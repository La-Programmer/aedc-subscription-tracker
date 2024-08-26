#!/usr/bin/python3
""" User API endpoints """
import requests.adapters
from models.user import User
from models import storage
from ..controllers.auth_controller import Auth, UserNotFound
import requests
import json
from redis import StrictRedis
from datetime import timedelta
from api.v1.views import app_views
from flask_jwt_extended import jwt_required, get_jwt
from flask import abort, jsonify, make_response, current_app, request

jwt_redis_blocklist = StrictRedis(
     host="redis", port=6379, db=0, decode_responses=True
  )
@app_views.route('/users', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_users():
    """Retrieves the list of all users
    """
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.make_user_response())
    return (jsonify(list_users)), 200

@app_views.route('/users/<user_id>', methods=['GET'],
        strict_slashes=False)
@jwt_required()
def get_user(user_id):
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict()), 200

@app_views.route('/users/<user_id>', methods=['DELETE'],
        strict_slashes=False)
@jwt_required()
def delete_user(user_id):
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
    auth = Auth()
    if not request.get_json():
        abort(400, description="Invalid JSON")

    if 'username' not in request.get_json():
        abort(400, description="Missing username")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    request_data = request.get_json()
    try:
        response = auth.authenticate(request_data)
        if response:
            access_token = auth.create_token(response['id'])
            if access_token:
                return(jsonify(user=response, token=access_token))
        else:
            abort(500, description="Access token could not be generated")
    except UserNotFound as e:
        current_app.logger.info(f"Authentication Failed: {str(e)}")
        abort(404, description=f"Authentication Failed: {str(e)}")
    except requests.exceptions.HTTPError as err:
        current_app.logger.info(f"Authentication Failed: {str(e)}")
        abort(err.response.status_code, description=f"Authentication Failed: {str(e)}")
    except Exception as e:
        current_app.logger.info(f"Authentication Failed: {str(e)}")
        abort(e.response.status_code, description=f"Authentication Failed: {str(e)}")


@app_views.route('/users/logout', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def logout():
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
    
    if not request.get_json():
        abort(400, description="Invalid JSON") 
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    user.update(data)
    user.save()
    current_app.logger.critical("User information has been updated")
    return make_response(jsonify(user.make_user_response()), 201)
