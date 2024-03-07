#!/usr/bin/env python3
""" basic authrization module """
from .session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ seasion with expire time """
    def __init__(self):
        """ initializes the class"""
        sd = os.getenv('SESSION_DURATION', '0')
        if sd.isnumeric():
            self.session_duration = int(sd)
        else:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ creates a session """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ get user by session """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None
        session_info = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_info["user_id"]
        if session_info.get('created_at') is None:
            return None
        expiry = session_info['created_at'] + timedelta(
            seconds=self.session_duration)
        if expiry < datetime.now():
            return None
        return session_info['user_id']
