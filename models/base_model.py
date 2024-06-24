#!/usr/bin/python3
"""This script is the base model"""

import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """
    Base class for all other classes.

    This class provides methods for initializing instance attributes,
    saving updated_at attribute, and converting to a dictionary.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes instance attributes.

        Args:
            - *args: list of arguments
            - **kwargs: dict of key-values arguments
        """

        if kwargs is not None and kwargs != {}:
            for key in kwargs:
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = kwargs[key]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """
        Returns official string representation.

        Returns:
            str: official string representation of the object.
        """

        return "[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """
        Updates the public instance attribute updated_at.

        This method updates the updated_at attribute of the object
        with the current datetime and saves the changes to the storage.
        """

        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of __dict__.

        This method creates a dictionary by copying the __dict__ of the object.
        It adds the __class__ key with the name of the class and converts the
        created_at and updated_at attributes to ISO format.

        Returns:
            dict: dictionary containing all keys/values of __dict__
        """

        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict["created_at"] = my_dict["created_at"].isoformat()
        my_dict["updated_at"] = my_dict["updated_at"].isoformat()
        return my_dict
