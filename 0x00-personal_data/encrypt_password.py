#!/usr/bin/env python3
""" password encrypting """
import bcrypt


def hash_password(password: str) -> bytes:
    """ password hasher """
    salt = bcrypt.gensalt()
    enc_pass = bcrypt.hashpw(password.encode('utf-8'), salt)

    return enc_pass


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ checkes a password's validity """
    return bcrypt.checkpw(password.encode(), hashed_password)
