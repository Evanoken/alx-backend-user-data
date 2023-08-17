#!/usr/bin/env python3
""" Auth module. """
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class. """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require auth. """
        # Check if path is None or excluded_paths is None or empty.
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        # Check if path ends with /.
        # Add / to path if it does not end with / to ensure strict matching.
        if path[-1] != '/':
            path += '/'
        # Handle excluded_paths ending with *.
        for excluded in excluded_paths:
            # If excluded ends with *.
            if excluded.endswith('*'):
                # Remove * from excluded.
                excluded_prefix = excluded[:-1]
                # Check if path starts with excluded up to the *.
                if path.startswith(excluded_prefix):
                    return False
            elif excluded.endswith('*/'):
                # Remove */ from excluded.
                excluded_prefix = excluded[:-2]
                # Check if path starts with excluded up to the *.
                if path.startswith(excluded_prefix):
                    return False
        # Check if path is in excluded_paths.
        if path in excluded_paths:
            return False
        # If path is not in excluded_paths, return True.
        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header. """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user. """
        return None
