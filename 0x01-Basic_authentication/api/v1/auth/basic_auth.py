#!/usr/bin/env python3
""" authrization module """
from .auth import Auth


class BasicAuth(Auth):
    """ authenitcation class"""
    def __init__(self) -> None:
        """ intializations """
        pass

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ base64 authorization header """
        if authorization_header is None or type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.lstrip('Basic ')