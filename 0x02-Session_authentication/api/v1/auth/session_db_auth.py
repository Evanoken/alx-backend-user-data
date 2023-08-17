#!/usr/bin/env python3
""" Session DB Auth module. """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ Session DB Auth class. """
    def create_session(self, user_id: str = None) -> str:
        """ Create Session method. """
        session_id = super().create_session(user_id)
        # Check if session_id is None
        if session_id is None:
            return None
        # Create a UserSession object with user_id and session_id
        user_session = UserSession(user_id=user_id, session_id=session_id)
        # Save the UserSession object to the database
        user_session.save()
        # Return the session ID
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ User ID for Session ID method. """
        # Check if session_id is None
        if session_id is None:
            return None
        # Check for session_id from the database
        try:
            user_session = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        # Check if user_session is empty meaning no session_id found
        if len(user_session) == 0:
            return None
        # Get the first element of the list
        user_session = user_session[0]
        # Check if session_duration is less than or equal to 0
        if self.session_duration <= 0:
            return user_session.user_id
        # Check if created_at exists
        created_at = user_session.created_at
        if created_at is None:
            return None
        # Check if session is expired
        expired_at = created_at + timedelta(seconds=self.session_duration)
        if expired_at < datetime.now():
            return None
        # Return the user_id
        return user_session.user_id

    def destroy_session(self, request=None) -> bool:
        """ Destroy Session method. """
        # Check if request is None
        if request is None:
            return False
        # Get the session_id from the cookie
        session_id = self.session_cookie(request)
        # Check if session_id is None
        if session_id is None:
            return False
        # Check for session_id from the database
        try:
            user_session = UserSession.search({"session_id": session_id})
        except Exception:
            return False
        # Check if user_session is empty meaning no session_id found
        if len(user_session) == 0:
            return False
        # Get the first element of the list and delete it
        try:
            user_session[0].remove()
        except Exception:
            return False
        # Return True if successful
        return True
