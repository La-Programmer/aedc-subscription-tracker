#!/usr/bin/python3
import os
from os import getenv
from ..celery_config import celery_init_app
from flasgger import Swagger
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import logging
from logging.config import dictConfig
# from celery.schedules import crontab
from flask_session import Session
from redis import Redis
from flask import Flask, make_response, jsonify, session

def create_app(test_config=None) -> Flask:
  """Create and configure flask application"""
  dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
       'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
      },
      'file': {
         'class': 'logging.FileHandler',
         'filename': 'app.log',
         'formatter': 'default'
      }
    },
    'root': {
        'level': 'CRITICAL',
        'handlers': ['wsgi', 'file'],
        'propagate': True
    }
})
  app = Flask(__name__, instance_relative_config=True)
  app.secret_key = getenv('SECRET_KEY')
  app.config.from_mapping(
    SECRET_KEY=getenv('SECRET_KEY'),
    CELERY=dict(
        broker_url="redis://localhost:6379/0",
        result_backend="redis://localhost:6379/0",
        task_ignore_result=True,
        broker_connection_retry_on_startup=True,
        beat_schedule={
           'task-every-10-seconds' : {
           "task": "api.v1.email_service.send_notification_email_task",
           "schedule": 10
        }
      }
    ),
    SWAGGER=dict(
        title='AEDC Subscription Tracking Application',
        uiversion=3
    ),
    JSONIFY_PRETTYPRINT_REGULAR=True,
    SESSION_TYPE = 'redis',
    SESSION_REDIS = Redis(host='localhost', port=6379)
  )

  Session(app)
  celery_init_app(app)
  app.register_blueprint(app_views)
  Swagger(app)
  logger = logging.getLogger(__name__)
  cors = CORS(app, resources={r"/*": {"origins": "*"}})

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
  
  @app.route('/hello')
  def hello():
    logger.critical("Application is up and running")
    return 'Hello, World!'
  
  return app
