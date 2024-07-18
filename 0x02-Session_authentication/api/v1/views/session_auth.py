#!/usr/bin/env python3
""" Module of Users session views
"""
from api.v1.views import app_views
from flask import jsonify, request
from os import getenv


@app_views.route('/auth_session/login',
                 methods=['POST'],
                 strict_slashes=False)
def session_login_handler():
    """Handles the session creation and login of users"""
    if request.method == "POST":
        email = request.form.get('email')
        if not email:
            return jsonify({"error": "email missing"}), 400

        paswd = request.form.get('password')
        if not paswd:
            return jsonify({"error": "password missing"}), 400

        from models.user import User

        user_by_mail = User.search({"email": email})

        if user_by_mail:
            for user in user_by_mail:
                if user.is_valid_password(paswd):
                    from api.v1.app import auth

                    user_data = user.to_json()
                    _session = auth.create_session(user_data.get('id'))
                    _response = jsonify(user_data)
                    # setting up the cookie inside the response
                    _response.set_cookie(getenv('SESSION_NAME'), _session)
                    return _response
                else:
                    return jsonify({"error": "wrong password"}), 401
        else:
            return jsonify({"error": "no user found for this email"}), 404
