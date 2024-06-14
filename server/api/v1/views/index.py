#!/usr/bin/python3
""" Index """
from models.subscription import Subscription
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify
from ..email_service import send_email_task

@app_views.route('/')
def begin():
  """ Starts app and background job """


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
  """ Status of API """
  return jsonify({"status": "OK"})
  