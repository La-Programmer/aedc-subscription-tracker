#!/usr/bin/python3
import os
import json
from dotenv import load_dotenv
from ..celery_config import celery_init_app
from flasgger import Swagger
from models import storage
from models.subscription import Subscription
from api.v1.views import app_views
from flask_cors import CORS
import requests
from redis import StrictRedis
import logging
from datetime import timedelta, datetime
from flask_jwt_extended import JWTManager
from flask import Flask, make_response, jsonify
from flask_mail import Mail, Message
from celery.schedules import crontab
from celery import shared_task
from flask_swagger_ui import get_swaggerui_blueprint


# load_dotenv(dotenv_path='/home/justin/aedc-subscription-tracker/server/.env.local')
REDIS = os.environ.get('REDIS')
SECRET = os.environ.get('SECRET_KEY')
JWT_REDIS = os.environ.get('JWT_REDIS')
def create_app(test_config=None) -> Flask:
  """Create and configure flask application"""
  app = Flask(__name__)
  app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
  app.config['MAIL_PORT'] = 2525
  app.config['MAIL_USERNAME'] = '0600ccec6a5dde'
  app.config['MAIL_PASSWORD'] = '0d97a6424e6d40'
  app.config['MAIL_USE_TLS'] = True
  app.config['MAIL_USE_SSL'] = False
  app.config.from_prefixed_env()
  app.config.from_mapping(
    SECRET_KEY=SECRET,
    CELERY=dict(
        broker_url=REDIS,
        result_backend=REDIS,
        task_ignore_result=True,
        broker_connection_retry_on_startup=True,
        beat_schedule={
           'periodic-task' : {
           "task": "api.v1.email_service.send_notification_email_task",
           "schedule": 100,#timedelta(days=1)
        }
      }
    ),
    JSONIFY_PRETTYPRINT_REGULAR=True,
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1),
    # JWT_COOKIE_SECURE = False,
    # JWT_TOKEN_LOCATION = ["cookies"],
    JWT_SECRET_KEY = SECRET,
    CORS_HEADERS = 'Content-Type'
    # JWT_TOKEN_EXPIRES = timedelta(hours=1)
  )

  SWAGGER_URL="/swagger"
  API_URL="/static/swagger.json"

  swagger_ui_blueprint = get_swaggerui_blueprint(
      SWAGGER_URL,
      API_URL,
      config={
          'app_name': 'Access API'
      }
  )
  app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
 
  celery_init_app(app)
  app.register_blueprint(app_views)
  logger = logging.getLogger('flask')
  cors = CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
  jwt = JWTManager(app)

  jwt_redis_blocklist = StrictRedis(
     host=JWT_REDIS, port=6379, db=0, decode_responses=True
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
    return make_response(jsonify(), 200)

  
  
    # print("Send email function has begun")
    # name = subscription.subscription_name
    # users = storage.get_users_associated_with_a_subscription(subscription.id)
    # print(f"Email sending to users of subscription {name}")
    # logger.critical(f"Email sending to users of subscription {name}")
    # mail = Mail(app)
    # # print('GOT HERE 1')
    # message = Message(
    #   subject=f"Email notification for {name}",
    #   recipients=users,
    #   sender="justinoghenekomeebedi@gmail.com"
    # )
    # # print('GOT HERE 2')
    # message.body = message_body
    # try:
    #   mail.send(message)
    #   logger.critical("Emails successfully sent")
    # except Exception as e:
    #   logger.critical(str(e))
    # try:
    #   print("Subscription object to update", subscription)
    #   logger.critical("ABOUT TO UPDATE SUBSCRIPTION OBJECT")
    #   subscription.update({'last_notification': datetime.now()})
    #   # subscription.save()
    #   logger.critical("SUBSCRIPTION UPDATED SUCCESSFULLY")
    #   # updated_subscription = storage.get(Subscription, subscription['id'])
    #   print("Updated subscription object", subscription)
    # except Exception as e:
    #   logger.critical(str(e))


  def send_first_email(subscription):
    """Send welcome email"""
    print("Welcome email sent to users")
  
  return app

