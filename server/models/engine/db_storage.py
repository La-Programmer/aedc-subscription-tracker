#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from sqlalchemy import create_engine, select
from models.base_model import Base, BaseModel
from models.user import User
from models.subscription import Subscription
from sqlalchemy.orm import scoped_session, sessionmaker
from os import environ


# declare classes
classes = {"User": User, "Subscription": Subscription}

class DBStorage:
  "Sets up MysqlDB storage"
  __engine = None
  __session = None

  def __init__(self):
    """Instantiate a DBStorage object"""
    USER=environ.get('USER')
    PASSWORD=environ.get('PASSWORD')
    HOST=environ.get('HOST')
    DB=environ.get('DB') 
    print(f'{USER}, {PASSWORD}, {HOST}, {DB}')
    self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
      USER,
      PASSWORD,
      HOST,
      DB
      ))
    
  def all(self, cls=None):
    """ Gets all objects of a specific class, or all classes """
    new_dict = {}
    for clss in classes:
      if cls is None or cls is classes[clss] or cls is clss:
        objs = self.__session.query(classes[clss]).all()
        for obj in objs:
          key = obj.__class__.__name__+'.'+obj.id
          new_dict[key] = obj
    return (new_dict)
  
  def get(self, cls, id):
    """ Gets an object of a class by ID """
    for clss in classes:
      if cls is classes[clss] or cls is  clss:
        obj = self.__session.query(classes[clss]).get(id)
    return (obj)
  
  def get_user_by_email(self, email):
    """ Gets a user by email """
    result = self.__session.query(User).filter_by(email=email).first()
    return(result)
  
  def new(self, obj):
    """Adds a newly created object to the DB session"""
    # print("Got here")
    # print(obj)
    self.__session.add(obj)

  def save(self):
    """Commits the current changes to the DB"""
    self.__session.commit()

  def close(self):
    """Call remove() method on the private session attribute"""
    self.__session.remove()

  def delete(self, obj=None):
    """ Delete an object from the database """
    if obj is not None:
      self.__session.delete(obj)

  def reload(self):
    """Reloads data from the database"""
    Base.metadata.create_all(self.__engine)
    sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
    Session = scoped_session(sess_factory)
    self.__session = Session