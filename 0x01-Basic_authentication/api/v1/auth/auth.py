""" authrization module """
from flask import request
from typing import TypeVar


class Auth:
    def __init__(self) -> None:
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ checks if authentication is required"""
        return False
    
    def authorization_header(self, request=None) -> str:
        """ checks header for authrization """
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """ checks the user """
        return None
