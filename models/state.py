#!/usr/bin/python3
"""This module creates a State class"""

from models.base_model import BaseModel


class State(BaseModel):
    """
    Class for managing state objects.

    Attributes:
        name (str): The name of the state.
    """

    name = ""
