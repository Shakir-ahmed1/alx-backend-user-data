#!/usr/bin/env python3
""" authrization module """
from flask import request
from typing import TypeVar, List


class Auth:
    """ authenitcation class"""
    def __init__(self) -> None:
        """ intializations """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ checks if authentication is required"""
        if not path or not excluded_paths:
            return True
        sh = path.rstrip('/') + '/'
        if sh in excluded_paths or path.rstrip('/') in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """ checks header for authrization """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ checks the user """
        return None
