#!/usr/bin/env python3
""" session authrization module """
from .auth import Auth
from uuid import uuid4


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
