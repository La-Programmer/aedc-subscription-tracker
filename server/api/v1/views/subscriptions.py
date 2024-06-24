#!/usr/bin/python3
""" Subscription API endpoints """
from models.subscription import Subscription
from models.user import User
from models import storage
from api.v1.views import app_views
from ..email_service import send_welcome_email_task
from flask import abort, jsonify, make_response, current_app, request, session
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
  
  current_app.logger.critical(f"Subscription {subscription.to_dict()['subscription_name']} has been deleted")
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
      type: string
      required: true
      description: The ID of the user
    - name: subscription_data
      in: body
      required: true
      requires:
        - subscription_name:
        - expiry_date:
        - users
        - subscription_cost
        - subscription_description
      properties:
        subscription_name:
          type: string
        start_date:
          type: string
        expiry_date:
          type: string
        users:
          type: string
        subscription_cost:
          type: integer
        subscription_description:
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
  print(subscription_creator)
  new_subscription = Subscription(subscription_creator, **request_data)
  # print(type(new_subscription))
  new_subscription.save()
  send_welcome_email_task(new_subscription)
  subscription_response = new_subscription.make_subscription_response()
  current_app.logger.critical(f"Subscription {subscription_response['subscription_name']} has been created")
  current_app.logger.critical(f"API STATUS {session['api_status']}")
  print(subscription_response)
  return make_response(jsonify(new_subscription.make_subscription_response()), 201)

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
  subscription_response = subscription.make_subscription_response()
  current_app.logger.critical(f"Subscription {subscription_response['subscription_name']} has been updated")
  return make_response(jsonify(subscription_response), 200)
