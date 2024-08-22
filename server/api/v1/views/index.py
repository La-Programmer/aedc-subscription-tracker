#!/usr/bin/python3
""" Index """
from api.v1.views import app_views
from flask import jsonify
from flasgger.utils import swag_from

# @app_views.route('/', methods=['GET'], strict_slashes=False)
# def begin():
#   """ Starts app and background job """
#   current_app.logger.critical("Application is up and running")
#   return 'WELCOME HOME'

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
  """ Status of API """
  return jsonify({'status': 'OK'})
  