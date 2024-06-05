#!/usr/bin/python3
""" Subscription API endpoints """
from models.subscription import Subscription
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request

@app_views.route('/subscriptions', methods=['GET'],
                 strict_slashes=False)
def get_subscriptions():
  """Retrieves a list of all subscriptions
  ---
  responses:
    200:
      description: All subscriptions gotten successfully
  """
  all_subscriptions = storage.all(Subscription).values()
  list_subscriptions = []
  for subscription in all_subscriptions:
    list_subscriptions.append(subscription.to_dict())
  return (jsonify(list_subscriptions)), 200

@app_views.route('/subscriptions/<subscription_id>', methods=['GET'],
                 strict_slashes=False)
def get_subscription(subscription_id):
  """ Gets a subscription by ID
  ---
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
  parameters:
  """
