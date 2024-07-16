#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from sqlalchemy import create_engine, update
from models.base_model import Base, BaseModel
from models.user import User
from models.subscription import Subscription
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(dotenv_path='/home/justin/aedc-subscription-tracker/server/.env.local')
# declare classes
classes = {"User": User, "Subscription": Subscription}

class DBStorage:
  "Sets up MysqlDB storage"
  __engine = None
  __session = None

  def __init__(self):
    """Instantiate a DBStorage object"""
    USER=os.environ.get("USER")
    PASSWORD=os.environ.get("PASSWORD")
    HOST=os.environ.get("HOST")
    DB=os.environ.get("DB") 
    # print(f'{USER}, {PASSWORD}, {HOST}, {DB}')
    self.__engine = create_engine(f"mysql+mysqldb://{USER}:{PASSWORD}@{HOST}:3306/{DB}")    

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
    # print("GOT HERE!!!!!!!!!!!")
    result = self.__session.query(User).filter_by(email=email).first()
    print("Result", result)
    return(result)
  
  def get_all_subscriptions_for_specific_user(self, user_id):
    """Gets all the subscriptions created by a user"""
    subscriptions = self.__session.query(Subscription).filter_by(created_by=user_id).all()
    result = [sub.make_subscription_response() for sub in subscriptions]
    return result


  def get_users_associated_with_a_subscription(self, subscription_id):
    """Gets the users associated with a subscription"""
    # print("GOT HERE!!!!!!!!!!!")
    subscription = self.__session.query(Subscription).filter_by(id=subscription_id).first()
    users = []
    for user in subscription.users:
      users.append(user.email)
    creator = self.get(User, subscription.created_by)
    users.append(creator.email)
    # print("Users associated with subscription", users)
    return(users)

  def new(self, obj):
    """Adds a newly created object to the DB session"""
    # print("Got here")
    # print(obj)
    self.__session.add(obj)

  def get_users_by_email_array(self, array):
    """Take an array of emails and replace them with their user instances"""
    result_array = [self.get_user_by_email(user) for user in array]
    return result_array

  
  def update(self, obj, kwargs):
    """Updates a record in DB"""
    print("Update begun")
    name = obj.__class__.__name__
    if name == 'Subscription':
      instance_object = self.__session.query(Subscription).filter_by(id=obj.id).first()
    elif name == 'User':
      instance_object = self.__session.query(User).filter_by(id=obj.id).first()
    print(f"Instance Object: {instance_object}")
    for key, value in kwargs.items():
      if key == 'users':
        value = self.get_users_by_email_array(value)
      setattr(instance_object, key, value)
    print(instance_object)
    print("Update ended")
    

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
