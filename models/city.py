#!/usr/bin/python3
"""This module creates a User class"""

from models.base_model import BaseModel


class City(BaseModel):
    """
    Class for managing city objects.

    Attributes:
        state_id (str): The ID of the state.
        name (str): The name of the city.
    """
    state_id = ""
    name = ""
