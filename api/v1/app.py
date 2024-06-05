#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, render_template, make_response, jsonify
# from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_db(error):
  """ Close storage"""
  storage.close()

@app.errorhandler(404)
def not_found(error):
  """ 404 Error
  ---
  responses:
    404:
      description: a resource was not found
  """
  return make_response(jsonify({'error': "Not found"}), 404)

app.config['SWAGGER'] = {
  'title': 'AEDC Subscription Tracking Applicaition',
  'uiversion': 3
}

Swagger(app)

if __name__ == "__main__":
  """Main Function"""
  host = '0.0.0.0'
  port = '5000'
  app.run(debug=True, host=host, port=port, threaded=True)
