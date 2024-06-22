#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, make_response, jsonify, session
from flasgger import Swagger
from celery.schedules import crontab
from ..celery_config import celery_init_app
from flask_cors import CORS
from os import getenv
# from dotenv import load_dotenv
# from redis.client import Redis
# from flask_session import Session
import logging

app = Flask(__name__)
# storage.init_app(app)
app.secret_key = getenv('SECRET_KEY')
app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost:6379/0",
        result_backend="redis://localhost:6379/0",
        task_ignore_result=True,
    ),
    SWAGGER=dict(
        title='AEDC Subscription Tracking Application',
        uiversion=3
    ),
    JSONIFY_PRETTYPRINT_REGULAR=True
    # SESSION_TYPE = 'redis'
)

# Session(app)
celery_app = celery_init_app(app)
app.register_blueprint(app_views)
Swagger(app)
logger = logging.getLogger(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
logging.basicConfig(filename='app.log', level=logging.DEBUG)

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


if __name__ == "__main__":
    """Main Function"""
    host = '0.0.0.0'
    port = '5000'
    app.run(debug=True, host=host, port=port, threaded=True)
