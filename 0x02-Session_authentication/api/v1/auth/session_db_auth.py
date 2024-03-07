#!/usr/bin/env python3
""" Session db module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ session db auth """
    def create_session(self, user_id=None):
        """ create a session """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        kw = {
            "user_id": user_id,
            "session_id": session_id
        }
        user = UserSession(**kw)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ user id for session id """
        # search_result = UserSession().search(
        # attributes={"session_id":session_id})
        # if not search_result:
        #     return None
        # return search_result[0].user_id
        if session_id is None:
            return None
        session_info = UserSession().search(
            attributes={'session_id': session_id})
        if not session_info:
            return None
        session_info = session_info[0]
        if self.session_duration <= 0:
            return session_info.user_id
        if session_info.created_at is None:
            return None
        expiry = session_info.created_at + timedelta(
            seconds=self.session_duration)

        if expiry < datetime.utcnow():
            return None

        return session_info.user_id

    def destroy_session(self, request=None):
        """ destroy session """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        search_result = UserSession().search(
            attributes={"session_id": session_id})
        if not search_result:
            return False
        search_result[0].remove()
        return True
