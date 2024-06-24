#!/usr/bin/python3
""" Index """
from models.subscription import Subscription
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, current_app, session, render_template
from ..email_service import send_notification_email_task

# @app_views.route('/', methods=['GET'], strict_slashes=False)
# def begin():
#   """ Starts app and background job """
#   current_app.logger.critical("Application is up and running")
#   return 'WELCOME HOME'

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
  """ Status of API """
  return jsonify({'status': 'OK'})
  