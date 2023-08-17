#!/usr/bin/env python3
""" Session Exp Auth module. """
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """ Session Exp Auth class. """
    def __init__(self):
        """ Initialize Session Exp Auth. """
        super().__init__()
        # Get session duration.
        session_duration_string = getenv("SESSION_DURATION")
        # Cast session duration to int.
        try:
            self.session_duration = int(session_duration_string)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """ Create session. """
        # Create session_id.
        session_id = super().create_session(user_id)
        # Check if session_id is None.
        if session_id is None:
            return None
        # Create session dictionary.
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        # Add session dictionary to user_id_by_session_id attribute.
        self.user_id_by_session_id[session_id] = session_dictionary
        # Return session_id.
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ User ID for session ID. """
        # Check if session_id is None.
        if session_id is None:
            return None
        # Check if user_id_by_session_id has session_id.
        session_data = self.user_id_by_session_id.get(session_id)
        if session_data is None:
            return None

        user_id = session_data.get("user_id")
        created_at = session_data.get("created_at")

        # Check if session duration is less than or equal to 0.
        if self.session_duration <= 0:
            return user_id
        # Check if created_at exists.
        if created_at is None:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        # Check if user session is expired.
        if expiration_time < datetime.now():
            return None
        # Return user_id.
        return user_id
