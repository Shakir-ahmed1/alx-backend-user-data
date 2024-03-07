#!/usr/bin/env python3
""" password hashing
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ password hasher """
    gen_salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), gen_salt)
