#!/usr/bin/env python3
""" session authrization module """
from .auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """ session authenitcation class"""
    user_id_by_session_id = {}

    def __init__(self) -> None:
        """ intializations """
        pass

    def create_session(self, user_id: str = None) -> str:
        """ creates a session for a user """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ return user id for session id """
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ returns a user based on cookie """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ deletes a session """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        self.user_id_by_session_id.pop(session_id)
        if user_id is None:
            return False
        return True
