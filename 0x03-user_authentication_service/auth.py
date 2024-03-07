#!/usr/bin/env python3
""" password hashing
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ password hasher """
    gen_salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), gen_salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ initialize the class"""
        self._db = DB()

    def register_user(self, email, password):
        """ registers a new user"""
        try:
            search = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
