#!/usr/bin/env python3

from celery import shared_task
import requests, json, os
from models import storage
from datetime import datetime
import logging
from models.subscription import Subscription
from dotenv import load_dotenv


logger = logging.getLogger('celery')
# load_dotenv(dotenv_path='/home/justin/aedc-subscription-tracker/server/.env.local')
@shared_task(ignore_result=False)
def send_notification_email_task():
    """ Task to handle email sending """
    # print("Background job send_notification_email_task started")
    logger.critical("DAILY CHECK FOR NOTIFICATIONS HAS BEGUN")
    subscriptions: 'list[Subscription]' = storage.all('Subscription')
    for subscription in subscriptions.values():
        subscription: Subscription
        # print(type(subscription.expiry_date))
        days_remaining = check_time_to_expiry_date(subscription.expiry_date)
        if days_remaining > 90:
            if check_last_notification_date(subscription) == 0 or check_last_notification_date(subscription) >= 30:
                print("GOT HERE")
                send_email(subscription, make_email_message(subscription.subscription_name, days_remaining))
        elif days_remaining < 90 and days_remaining > 60:
            if check_last_notification_date(subscription) == 0 or check_last_notification_date(subscription) >= 15:
                print("GOT HERE")
                send_email(subscription, make_email_message(subscription.subscription_name, days_remaining))
        elif days_remaining < 60 and days_remaining > 30:
            if check_last_notification_date(subscription) == 0 or check_last_notification_date(subscription) >= 7:
                print("GOT HERE")
                send_email(subscription, make_email_message(subscription.subscription_name, days_remaining))
        elif days_remaining < 30:
            if check_last_notification_date(subscription) == 0 or check_last_notification_date(subscription) >= 1:
                print("GOT HERE")
                send_email(subscription, make_email_message(subscription.subscription_name, days_remaining))
        elif days_remaining <= 0:
            print("GOT HERE")
            send_email(subscription, make_email_message(subscription.subscription_name, days_remaining))
            subscription.update(subscription_status=False)
            subscription.delete()

def make_email_message(name, days):
    """Returns the subscription string"""
    return f"This is to notify you that your subscription {name} will expire in {days} days."

def send_welcome_email_task(subscription: Subscription):
    """Task to handle sending welcome email"""
    name = subscription.subscription_name
    message_body = "This is to notify you that the subscription f{name} is now being tracked"
    send_email(subscription, message_body)

def check_time_to_expiry_date(expiry_date):
    """ Function to check how long to the expiry date
    of a subscription
    """
    # expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d %H:%M:%S')
    days_remaining = datetime.now() - expiry_date
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
    users.append('justinoghenekomeebedi@gmail.com')
    payload = {
        "subject": 'SUBSCRIPTION NOTIFICATION',
        "body": message_body,
        "deliveryAddressArray": users,
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
            count += 1
    return False
