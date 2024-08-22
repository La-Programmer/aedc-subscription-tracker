#!/usr/bin/env python3

from dotenv import load_dotenv
from flask_jwt_extended import create_access_token
from models.user import User
from models import storage
import os
import requests


load_dotenv()


# CUSTOM AUTHENTICATION BASED EXCEPTION
class UserNotFound(Exception):
    """User not found exception"""
    def __init__(self, message):
        self.message = message
        super().__init__(message)
    
    def __str__(self):
        return f"Authenticaton Failed: {self.message}"


class Auth():
    """Authentication class"""
    def __init__(self):
        self._db = storage
    
    def register_user(self, user_info: dict) -> dict | None:
        """Register unregistered user"""
        try:
            new_user: User = User(**user_info)
            new_user.save()
            return new_user
        except Exception as e:
            raise
    
    def create_token(self, id: str) -> str | None:
        """Create access token for a user"""
        if id:
            try:
                token: str = create_access_token(identity=id)
                return token
            except Exception as e:
                raise
        else:
            return None
    
    def construct_user_object(self, user_info: dict) -> dict | None:
        """Construct a user object"""
        if (user_info):
            user_object: dict = {
                'email': user_info['mail'],
                'first_name': user_info['firstname'],
                'last_name': user_info['surname']
            }
            return user_object
        else:
            return None
        
    def login_or_register(self, user_info) -> dict | None:
        """Handle whether to login a user or register the user"""
        if user_info:
            user_object: dict = self.construct_user_object(user_info)
            user_email = user_object['email']
            user: User = storage.get_user_by_email(user_email)
            if (user):
                return user
            try:
                new_user: User = self.register_user(user_object)
                return new_user
            except Exception as e:
                raise
        else:
            return None
    
    def call_ad_service(self, request_data) -> dict | None:
        """Handle user auth using AD service"""
        if request_data:
            auth_endpoint = os.environ.get('AUTH_END_PONT')
            num = 0
            while num <= 5:
                try:
                    response = requests.post(
                        auth_endpoint,
                        json=request_data,
                    )
                    response_json = response.json()
                    status_code = response_json['status_code']
                    if status_code == '404':
                        num += 1
                        raise UserNotFound("Incorrect Username or Password")
                    if status_code == '200':
                        break
                except ConnectionError as e:
                    print(str(e))
                    num += 1
                    raise
                except Exception as e:
                    print(str(e))
                    num += 1
                    raise
            if response_json:
                return response_json['data']
            return None
        return None
    
    def authenticate(self, request_data) -> dict | None:
        """Handle all authentication logic"""
        username = request_data['username']
        password = request_data['password']
        if username and password:
            try:
                user_info = self.call_ad_service(request_data)
                if user_info is None:
                    return None
                try:
                    user: User = self.login_or_register(user_info)
                    if user is None:
                        return None
                except Exception as e:
                    raise e
            except Exception as e:
                raise
            response: dict = user.make_user_response()
            return response
        return None
