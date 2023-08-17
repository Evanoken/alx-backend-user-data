#!/usr/bin/env python3
""" User Session module. """
from models.base import Base
from typing import TypeVar, List, Iterable, Dict


class UserSession(Base):
    """ User Session class. """
    def __init__(self, *args: List, **kwargs: Dict) -> None:
        """ Initialize User Session. """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id", None)
        self.session_id = kwargs.get("session_id", None)
