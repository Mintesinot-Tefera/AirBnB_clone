#!/usr/bin/python3
"""This module creates a Review class"""

from models.base_model import BaseModel


class Review(BaseModel):
    """
    Class for managing review objects.

    Attributes:
        place_id (str): The ID of the place.
        user_id (str): The ID of the user.
        text (str): The review text.
    """
    place_id = ""
    user_id = ""
    text = ""
