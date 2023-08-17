#!/usr/bin/env python3
""" Module of Session Authentication views. """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    Return:
      - User instance JSON represented
    """
    # Get email and password from request.form.
    email = request.form.get('email')
    if not email or email == '':
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password or password == '':
        return jsonify({"error": "password missing"}), 400
    # Search user by email.
    try:
        user = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    # Check if user exists and password is valid.
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    # Create session and return user.
    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    cookie_name = getenv('SESSION_NAME')
    response = jsonify(user[0].to_json())
    response.set_cookie(cookie_name, session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """ DELETE /api/v1/auth_session/logout
    Return:
      - Empty JSON
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
