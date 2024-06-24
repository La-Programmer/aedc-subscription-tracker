#!/usr/bin/python3
from celery import shared_task
from models import storage
from datetime import datetime, timedelta

@shared_task(ignore_result=False)
def send_notification_email_task():
  """ Task to handle email sending """
  print("Background job send_notification_email_task started")
  subscriptions = storage.all('Subscription')
  # print(subscriptions)
  for subscription in subscriptions:
    days_remaining = check_time_to_expiry_date(subscription.expiry_date)
    if (days_remaining > 90):
      print("GOT HERE!!!!!")
      days_passed = check_last_notification_date(subscription.last_notification)
      print("Days passed", days_passed)
      if (days_passed >= 30 or days_passed == 0):
        send_email(subscription)
    elif (days_remaining <= 90 and days_remaining > 60):
      days_passed = check_last_notification_date(subscription.last_notification)
      if (days_passed >= 7 or days_passed == 0):
        send_email(subscription)
    elif (days_remaining <= 60 and days_remaining > 30):
      days_passed = check_last_notification_date(subscription.last_notification)
      if (days_passed >= 3.5 or days_passed == 0):
        send_email(subscription)
    elif (days_remaining <= 30):
      days_passed = check_last_notification_date(subscription.last_notification)
      if (days_passed >= 1 or days_passed == 0):
        send_email(subscription)

@shared_task(ignore_result=False)
def send_welcome_email_task(subscription):
  """Task to handle sending welcome email"""
  print("Background job send_welcome_email_task started")
  send_first_email(subscription)

def check_time_to_expiry_date(expiry_date):
  """ Function to check how long to the expiry date
  of a subscription
  """
  expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d:%H:%M')
  time_difference = expiry_date - datetime.utcnow()
  print("Time difference", time_difference)
  days_remaining = time_difference.total_seconds() / 60
  print("Days remaining", days_remaining)
  return days_remaining

def check_last_notification_date(last_notification_date):
  """ Function to check the last notification date of a subscription"""
  if not last_notification_date:
    return 0
  last_notification_date = datetime.strptime(last_notification_date, '%Y-%m-%d:H:%M')
  time_difference = datetime.utcnow() - last_notification_date
  print("Time difference 2", time_difference)
  days_passed = time_difference.total_seconds() / 60
  print("Days passed", days_passed)
  return days_passed

def send_email(subscription):
  """Send reminder email"""
  print("Email sent to Users")
  setattr(subscription, "last_notification", datetime.utcnow())

def send_first_email(subscription):
  """Send welcome email"""
  print("Welcome email sent to users")
  