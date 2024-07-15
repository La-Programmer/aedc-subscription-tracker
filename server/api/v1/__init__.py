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
import logging
from logging.config import dictConfig
import requests
from redis import StrictRedis
from datetime import timedelta, datetime
from flask_jwt_extended import JWTManager
from flask import Flask, make_response, jsonify
from flask_mail import Mail, Message
from celery.schedules import crontab
from celery import shared_task


load_dotenv()
REDIS = os.environ.get('REDIS_LOCAL')
SECRET = os.environ.get('SECRET_KEY')
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
           'task-every-10-seconds' : {
           "task": "api.v1.send_notification_email_task",
           "schedule": 20,#timedelta(days=1)
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
    JWT_SECRET_KEY = SECRET,
    CORS_HEADERS = 'Content-Type'
    # JWT_TOKEN_EXPIRES = timedelta(hours=1)
  )
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

  
  @shared_task(ignore_result=False)
  def send_notification_email_task():
    """ Task to handle email sending """
    # print("Background job send_notification_email_task started")
    subscriptions: 'list[Subscription]' = storage.all('Subscription')
    for subscription in subscriptions.values():
      subscription: Subscription
      # print(type(subscription.expiry_date))
      days_remaining = check_time_to_expiry_date(subscription.expiry_date)
      if days_remaining > 90:
        if check_last_notification_date(subscription) == 0 or check_last_notification_date(subscription) >= 30:
          print("GOT HERE")
          send_email(subscription, make_email_message(subscription.subscription_name, days_remaining)).delay()
      elif days_remaining < 90 and days_remaining > 60:
        if check_last_notification_date(subscription) == 0 or check_last_notification_date(subscription) >= 15:
          print("GOT HERE")
          send_email(subscription, make_email_message(subscription.subscription_name, days_remaining)).delay()
      elif days_remaining < 60 and days_remaining > 30:
        if check_last_notification_date(subscription) == 0 or check_last_notification_date(subscription) >= 7:
          print("GOT HERE")
          send_email(subscription, make_email_message(subscription.subscription_name, days_remaining)).delay()
      elif days_remaining < 30:
        if check_last_notification_date(subscription) == 0 or check_last_notification_date(subscription) >= 1:
          print("GOT HERE")
          send_email(subscription, make_email_message(subscription.subscription_name, days_remaining)).delay()
      elif days_remaining <= 0:
        print("GOT HERE")
        send_email(subscription, make_email_message(subscription.subscription_name, days_remaining)).delay()
        subscription.update(subscription_status=False)

  def make_email_message(name, days):
    """Returns the subscription string"""
    return f"This is to notify you that your subscription {name} will expire in {days} days."

  @shared_task(ignore_result=False)
  def send_welcome_email_task(subscription):
    """Task to handle sending welcome email"""
    print("Background job send_welcome_email_task started")
    send_first_email(subscription)

  def check_time_to_expiry_date(expiry_date):
    """ Function to check how long to the expiry date
    of a subscription
    """
    # expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d %H:%M:%S')
    days_remaining = expiry_date - datetime.now()
    return days_remaining.days

  def check_last_notification_date(subscription: Subscription):
    """ Function to check the last notification date of a subscription"""
    last_notification_date = subscription.last_notification
    if not last_notification_date:
      return 0
    days_passed = datetime.utcnow() - last_notification_date
    return days_passed.days

  @shared_task(ignore_result=False)
  def send_email(subscription: Subscription, message_body=None):
    """Send reminder email"""
    name = subscription.subscription_name
    users = storage.get_users_associated_with_a_subscription(subscription.id)
    payload = {
        "subject": 'SUBSCRIPTION NOTIFICATION',
        "body": message_body,
        "delivery_address": users,
        "type": 'One-time', # specify number of times the email should be sent
        "frequency": 0, # specify the frequency of delivery 0 is the default value
        "app_url": "https://subscriptions.abujaelectricity.com", # specify your app's url 
        "template": 'default' # select your template choice
    }

    headers = {
    'api-token': f'{os.environ.get("API_TOKEN")}',
    }

    email_api_endpoint = os.environ.get("END_POINT")
    email_sent = False
    count = 0
    while not email_sent and count <= 5:
        try:
            response = requests.post(email_api_endpoint, json=payload, headers=headers)
            # return response.status_code == 200
            res = json.dumps(response.json())
            if response.status_code == 200:
                email_sent = True
                logger.critical("Email sent successfully")
                subscription.update({'last_notification': datetime.now()})
                return True
            else:
                logger.critical(f"Email message request sent but response is {response.status_code}")
                count += 1
            logger.critical(f"-- API RESPONSE HERE  -- {res} ")
        except Exception as e:
            logger.critical(f"Request to send email NOT sent due to error {e}")
    return False
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

