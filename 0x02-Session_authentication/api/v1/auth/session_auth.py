#!/usr/bin/env python3
""" Session Auth module. """
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ Session Auth Class. """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create session. """
        # Check if user_id is None.
        if user_id is None:
            return None
        # Check if user_id is not a string.
        if not isinstance(user_id, str):
            return None
        # Create session_id.
        session_id = str(uuid.uuid4())
        # Add session_id to user_id_by_session_id attribute.
        self.user_id_by_session_id[session_id] = user_id
        # Return session_id.
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ User ID for session ID. """
        # Check if session_id is None.
        if session_id is None:
            return None
        # Check if session_id is not a string.
        if not isinstance(session_id, str):
            return None
        # Return user_id.
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Current user. """
        # Get cookie value.
        cookie_value = self.session_cookie(request)
        # Get user_id from cookie value.
        user_id = self.user_id_for_session_id(cookie_value)
        # Return user_id.
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ Deletes the user session / logout. """
        # Check if request is None.
        if request is None:
            return False
        # Get cookie value.
        cookie_value = self.session_cookie(request)
        # Check if cookie_value is None.
        if cookie_value is None:
            return False
        # Get user_id from cookie value.
        user_id = self.user_id_for_session_id(cookie_value)
        # Check if user_id is None.
        if user_id is None:
            return False
        # Delete user_id from user_id_by_session_id.
        del self.user_id_by_session_id[cookie_value]
        return True
