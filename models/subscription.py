#!/usr/bin/python3
"""Subscription model class declaration"""

from models.base_model import BaseModel , Base
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table
from datetime import datetime
from sqlalchemy.orm import relationship

user_subscriptions = Table('user_subscriptions', Base.metadata,
                          Column('user_id', String(60),
                                 ForeignKey('users.id', onupdate='CASCADE',
                                           ondelete='CASCADE'),
                                           primary_key=True),
                          Column('subscription_id', String(60),
                                 ForeignKey('subscriptions.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                            primary_key=True))

class Subscription(BaseModel, Base):
  "Subscription model class declaration"
  __tablename__ = 'subscriptions'
  subscription_name = Column(String(1024), nullable=False)
  subscription_status = Column(Boolean, nullable=False)
  start_date = Column(DateTime, default=datetime.now(), nullable=False)
  expiry_date = Column(DateTime, nullable=False)
  last_notification = Column(DateTime, default=None)
  created_by = Column(String(60), ForeignKey('users.id'), nullable=False)
  users = relationship("User",
                       secondary=user_subscriptions,
                       viewonly=False)

  def __init__(self, *args, **kwargs):
    "Iinitializes user"
    super().__init__(*args, **kwargs)
