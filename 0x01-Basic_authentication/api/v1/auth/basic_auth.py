#!/usr/bin/env python3
""" basic authrization module """
from .auth import Auth
from typing import TypeVar
import base64
from models.user import User


class BasicAuth(Auth):
    """ authenitcation class"""
    def __init__(self) -> None:
        """ intializations """
        pass

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ base64 authorization header """
        if authorization_header is None or type(authorization_header
                                                ) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.lstrip('Basic ')

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ decode base64 """
        if base64_authorization_header is None or type(
            base64_authorization_header
                                        ) is not str:
            return None
        try:

            return base64.b64decode(base64_authorization_header
                                    ).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ extract user credentials """
        if decoded_base64_authorization_header is None or type(
            decoded_base64_authorization_header
                                        ) is not str:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        user = decoded_base64_authorization_header.split(':')
        return (tuple(user))

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ get user object """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            search_result = User.search(attributes={"email": user_email})
            if not search_result:
                return None
            if not search_result[0].is_valid_password(user_pwd):
                return None
            return search_result[0]
        except KeyError:
            return None
