#!/usr/bin/python3
from os import getenv
from ..celery_config import celery_init_app
from flasgger import Swagger
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import logging
from logging.config import dictConfig
from redis import StrictRedis
from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask import Flask, make_response, jsonify
from flask_mail import Mail

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
  app = Flask(__name__)
  app.config.from_mapping(
    SECRET_KEY=getenv('SECRET_KEY'),
    CELERY=dict(
        broker_url="redis://localhost:6379/0",
        result_backend="redis://localhost:6379/0",
        broker_connection_retry_on_startup = True,
        task_ignore_result=True,
        beat_schedule={
           'task-every-10-seconds' : {
           "task": "api.v1.email_service.send_notification_email_task",
           "schedule": 10#timedelta(days=1)
        }
      }
    ),
    SWAGGER=dict(
        title='AEDC Subscription Tracking Application',
        uiversion=3
    ),
    JSONIFY_PRETTYPRINT_REGULAR=True,
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1),
    # JWT_COOKIE_SECURE = False,
    # JWT_TOKEN_LOCATION = ["cookies"],
    JWT_SECRET_KEY = getenv('SECRET_KEY'),
    CORS_HEADERS = 'Content-Type'
    # JWT_TOKEN_EXPIRES = timedelta(hours=1)
  )
  app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
  app.config['MAIL_PORT'] = 2525
  app.config['MAIL_USERNAME'] = '0600ccec6a5dde'
  app.config['MAIL_PASSWORD'] = '0d97a6424e6d40'
  app.config['MAIL_USE_TLS'] = True
  app.config['MAIL_USE_SSL'] = False
  app.config.from_prefixed_env()


  Mail(app)
  celery_init_app(app)
  app.register_blueprint(app_views)
  Swagger(app)
  logger = logging.getLogger(__name__)
  cors = CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
  jwt = JWTManager(app)

  jwt_redis_blocklist = StrictRedis(
     host="localhost", port=6379, db=0, decode_responses=True
  )

  @jwt.token_in_blocklist_loader
  def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
     jti = jwt_payload["jti"]
     token_in_redis = jwt_redis_blocklist.get(jti)
     return token_in_redis is not None

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
  
  @app.route('/')
  def hello():
    logger.critical("Application is up and running")
  
  return app
