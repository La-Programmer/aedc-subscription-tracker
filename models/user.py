#!/usr/bin/python3
"""User model class declaration"""

from models.base_model import BaseModel, Base
from models.subscription import Subscription
from sqlalchemy import Column, String, Table, ForeignKey

class User(BaseModel, Base):
  """User model class declaration"""
  __tablename__ = 'users'
  first_name = Column(String(128), nullable=False)
  last_name =  Column(String(128), nullable=False)
  email =  Column(String(128), nullable=False)
  
  def __init__(self, *args, **kwargs):
    "Iinitializes user"
    super().__init__(*args, **kwargs)
    print("New User successfully created")
  
  def create_subscription(self, *args, **kwargs):
    "User creates a subscription"
    kwargs["created_by"] = self.id
    new_subscription = Subscription(**kwargs)
    print("New subscription created by user {}: {}".format(self.first_name,
                                                           new_subscription))
    return(new_subscription)
    
