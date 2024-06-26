#!/usr/bin/python3
""" Subscription API endpoints """
from models.subscription import Subscription
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from datetime import datetime

@app_views.route('/subscriptions', methods=['GET'],
                 strict_slashes=False)
def get_subscriptions():
  """Retrieves a list of all subscriptions
  ---
  tags: S
  responses:
    200:
      description: All subscriptions gotten successfully
  """
  all_subscriptions = storage.all(Subscription).values()
  # print(all_subscriptions)
  list_subscriptions = []
  for subscription in all_subscriptions:
    list_subscriptions.append(subscription.make_dashboard_response())
  return (jsonify(list_subscriptions)), 200

@app_views.route('/subscriptions/<subscription_id>', methods=['GET'],
                 strict_slashes=False)
def get_subscription(subscription_id):
  """ Gets a subscription by ID
  ---
  tags: S
  parameters:
    - name: subscription_id
      in: path
      type: string
      required: true
      description: The ID of the subscription
  responses:
    200:
      description: Subscription information gotten successfully
    404:
      description: Subscription not found
  """
  subscription = storage.get(Subscription, subscription_id)
  if not subscription:
    abort(404)
  return jsonify(subscription.to_dict()), 200

@app_views.route('/subscription/<subscription_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_subscription(subscription_id):
  """ Deletes a subscription object
  ---
  tags: S
  parameters:
    - name: subscription_id
      in: path
      type: string
      required: true
      description: The ID of the subscription
  responses:
    204:
      description: Subscription deleted successfully
    404:
      description: Subscription not found
  """
  subscription = storage.get(Subscription, subscription_id)
  if not subscription:
    abort(404)
  
  subscription.delete()
  storage.save()
  return make_response(jsonify({}), 204)

@app_views.route('/subscriptions/<user_id>', methods=['POST'],
                 strict_slashes=False)
def create_subscription(user_id):
  """ Creates a subscription object
  ---
  tags: S
  parameters:
    - name: user_id
      in: path
      required: true
      description: The ID of the user creating the subscription
    - name: subscription_data
      in: body
      required: true
      requires:
        - subscription_name:
        - expiry_date:
        - users
      properties:
        subscription_name:
          type: string
        start_date:
          type: string
        expiry_date:
          type: string
        users:
          type: string
  responses:
    201:
      description: Subscription created successfully
    400:
      description: Invalid JSON or missing parameters

  """
  if not request.get_json():
    abort(400, description="Invalid JSON")
  
  if 'subscription_name' not in request.get_json():
    abort(400, description="Missing subscription name")
  if 'start_date' not in request.get_json():
    abort(400, description="Missing start date")
  if 'expiry_date' not in request.get_json():
    abort(400, description="Missing expiry date")
  if 'users' not in request.get_json():
    abort(400, description="Missing stakeholder emails")
  
  request_data = request.get_json()
  subscription_creator = storage.get(User, user_id)
  # print(type(subscription_creator))
  new_subscription = Subscription(subscription_creator, **request_data)
  # print(type(new_subscription))
  new_subscription.save()
  print(new_subscription.to_dict())
  return make_response(jsonify(new_subscription.to_dict()), 201)

@app_views.route('/subscriptions/<subscription_id>', methods=['PUT'],
                 strict_slashes=False)
def update_subscription(subscription_id):
  """ Updates a subscription object
  ---
  tags: S
  parameters:
      - name: subscription_id
        in: path
        required: true
        description: The ID of the subscription to be updated
      - name: subscription_data
        in: body
        required: true
        requires:
          - subscription_name:
          - expiry_date:
          - users
        properties:
          subscription_name:
            type: string
          expiry_date:
            type: string
          users:
            type: string
  responses:
    201:
      description: Subscription updated successfully
    400:
      description: Invalid JSON or missing parameters

  """
  subscription = storage.get(Subscription, subscription_id)
  if not subscription:
    abort(404)
  if not request.get_json():
    abort(400, description="Invalid JSON")
  
  ignore = ['id', 'created_at', 'updated_at']

  data = request.get_json()
  for key, value in data.items():
    if key not in ignore:
      if key in data.keys():
        setattr(subscription, key, value)
  subscription.save()
  return make_response(jsonify(subscription.to_dict()), 200)
