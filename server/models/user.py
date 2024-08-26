#!/usr/bin/python3
"""User model class declaration"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String

class User(BaseModel, Base):
  """User model class declaration"""
  __tablename__ = 'users'
  first_name = Column(String(128), nullable=False)
  last_name =  Column(String(128), nullable=False)
  email =  Column(String(128), nullable=False)
  
  def __init__(self, *args, **kwargs):
    "Iinitializes user"
    super().__init__(*args, **kwargs)
  
  def make_user_response(self):
    """Makes user response for front-end"""
    user_dict = self.to_dict()
    result = {}
    keys = ['email', 'first_name', 'last_name', 'id']
    for key in user_dict.keys():
      if key in keys:
        result[key] = user_dict[key]
    return result
