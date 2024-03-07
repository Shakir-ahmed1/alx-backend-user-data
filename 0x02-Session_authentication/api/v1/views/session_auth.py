#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """ POST /ap/i/v1/auth_session/login
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400

    search_result = User.search(attributes={"email": email})
    if not search_result:
        return jsonify({"error": "no user found for this email"}), 404
    user = search_result[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    else:
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        ret = jsonify(user.to_json())
        ret.set_cookie(os.getenv('SESSION_NAME'), session_id)
        return ret


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def delete_session() -> str:
    """ DELETE /api/v1/auth_session/logout
    """
    from api.v1.app import auth
    result = auth.destroy_session(request)
    if not result:
        abort(404)
    return jsonify({}), 200
