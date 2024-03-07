#!/usr/bin/env python3
""" Main 0
"""
from api.v1.auth.auth import Auth

a = Auth()

paths = ["/api/v1/stat*"]
print(a.require_auth("/api/v1/status", paths))
print(a.require_auth("/api/v1/users", paths))
print(a.require_auth("/api/v1/stats/", paths))
print(a.authorization_header())
print(a.current_user())
