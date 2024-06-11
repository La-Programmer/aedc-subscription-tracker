#!/usr/bin/python3

from models.user import User
from models.engine.db_storage import DBStorage
from datetime import datetime, timedelta

db = DBStorage()

new_user = User(first_name="Justin",
                last_name="Ebedi",
                email="justinoghenekomebedi@gmail.com")

print(new_user)
db.reload()
db.new(new_user)
db.save()
new_sub = new_user.create_subscription(subscription_name="Data subcription",
                             subscription_status=True,
                             start_date=datetime.today(),
                             expiry_date=datetime.today() + timedelta(days=10),
                             last_notification=datetime.today(),
                             users=[new_user])
db.new(new_sub)
db.save()
