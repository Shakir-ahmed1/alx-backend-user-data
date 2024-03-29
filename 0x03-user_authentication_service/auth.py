#!/usr/bin/env python3
""" password hashing
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """ password hasher """
    gen_salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), gen_salt)


def _generate_uuid() -> str:
    """ generate uuid """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        """ initialize the class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ registers a new user"""
        try:
            search = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """ check if the log in is valid """
        try:
            search = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  search.hashed_password)

        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ create new session """
        search = self._db.find_user_by(email=email)
        uid = _generate_uuid()
        self._db.update_user(search.id, session_id=uid)
        return uid

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ returns a user from session id"""
        if session_id is None:
            return None
        try:
            search = self._db.find_user_by(session_id=session_id)
            return search

        except NoResultFound:
            return None

    def destroy_session(self, user_id: str):
        """ destroys a session """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ reset password token """
        try:
            search = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(search.id, reset_token=reset_token)
            return reset_token

        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ update user password """
        try:
            search = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(search.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None)

        except NoResultFound:
            raise ValueError
