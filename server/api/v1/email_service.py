#!/usr/bin/env python3

from celery import shared_task
import requests, json, os
from models import storage
from dotenv import load_dotenv


# load_dotenv(dotenv_path='/home/justin/aedc-subscription-tracker/server/.env.local')
@shared_task(ignore_result=False)
def send_welcome_email_task(subscription):
    """Task to handle sending welcome email"""
    name = subscription.subscription_name
    message_body = f"This is to notify you that the subscription for {name} is now being tracked."
    users = storage.get_users_associated_with_a_subscription(subscription.id)
    users.append('justinoghenekomeebedi@gmail.com')
    print("Users", users)
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
                print("Email sent successfully")
                return True
            else:
                print(f"Email message request sent but response is {response.status_code}")
                count += 1
            print(f"-- API RESPONSE HERE  -- {res} ")
        except Exception as e:
            print(f"Request to send email NOT sent due to error {e}")
    return False
