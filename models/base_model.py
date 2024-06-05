#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

time = "%Y-%m-%dT%H:%M:%S.%f"

Base = declarative_base()

class BaseModel:
  """Base model class"""
  id = Column(String(60), primary_key=True)
  created_at = Column(DateTime, default=datetime.now, nullable=False)
  updated_at = Column(DateTime, default=datetime.now, nullable=False)

  def __init__(self, *args, **kwargs):
    """Base model initialization"""
    if kwargs:
      for key, value in kwargs.items():
        if key != "__class__":
          setattr(self, key, value)
      if kwargs.get("created_at", None) and type(self.created_at)  is str:
        self.created_at = datetime.strptime()
      else:
        self.created_at = datetime.now()
      if kwargs.get("updated_at", None) and type(self.updated_at) is str:
        self.updated_at = datetime.strptime(kwargs["updated_at"], time)
      else:
        self.updated_at = datetime.now()
      if kwargs.get("id", None) is None:
        self.id = str(uuid.uuid4())
    else:
      self.id = str(uuid.uuid4())
      self.created_at = datetime.now()
      self.updated_at = self.created_at
  
  def __str__(self):
    "Custom string representaition of the BaseModel class"
    return "{}\n{}\n{}\n".format(self.__class__.__name__,
                               self.id,
                               self.__dict__)
  
  def save(self):
    """Saves changes made to object"""
    self.updated_at = datetime.now()
    models.storage.new(self)
    models.storage.save()


  def to_dict(self):
    """Returns a dictionary representation of all key/values of the instance"""
    new_dict = self.__dict__.copy()
    if "created_at" in new_dict:
      new_dict["created_at"] = new_dict["created_at"].strftime(time)
    if "updated_at" in new_dict:
      new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
    new_dict["__class__"] = self.__class__.__name__
    if "_sa_instance_state" in new_dict:
      del new_dict["_sa_instance_state"]
    
    return new_dict
  
  def delete(self):
    """Delete the current instance from storage"""
    pass
