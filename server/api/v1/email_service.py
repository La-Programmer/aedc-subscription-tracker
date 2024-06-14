#!/usr/bin/python3
from celery import shared_task
from models import storage
from datetime import datetime, timedelta

@shared_task(ignore_result=False)
def send_email_task():
  """ Task to handle email sending """
  subscriptions = storage.all("Subscription")
  for subscription in subscriptions:
    days_remaining = check_time_to_expiry_date(subscription.expiry_date)
    if (days_remaining > 90):
      days_passed = check_last_notification_date(subscription.last_notification)
      if days_passed >= 30:
        send_email(subscription)
    elif (days_remaining <= 90 and days_remaining > 60):
      days_passed = check_last_notification_date(subscription.last_notification)
      if days_passed >= 7:
        send_email(subscription)
    elif (days_remaining <= 60 and days_remaining > 30):
      days_passed = check_last_notification_date(subscription.last_notification)
      if days_passed >= 3.5:
        send_email(subscription)
    elif (days_remaining <= 30):
      days_passed = check_last_notification_date(subscription.last_notification)
      if days_passed >= 1:
        send_email(subscription)
  

def check_time_to_expiry_date(expiry_date):
  """ Function to check how long to the expiry date
  of a subscription
  """
  time_difference = expiry_date - datetime.utcnow()
  days_remaining = time_difference.total_seconds() / 60
  return days_remaining

def check_last_notification_date(last_notification_date):
  """ Function to check the last notification date of a subscription"""
  if not last_notification_date:
    return
  time_difference = datetime.utcnow() - last_notification_date
  days_passed = time_difference.total_seconds() / 60
  return days_passed

def send_email(subscription):
  print("Email sent to Users")
  setattr(subscription, "last_notification", datetime.utcnow())
