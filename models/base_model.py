#!/usr/bin/python3
"""
BaseModel module
"""
import uuid
# import models
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()


class BaseModel:
    """
    Defines all common attributes/methods for other classes
    """

    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        Object initialiser
        """
        # from models import storage
        if kwargs:
            for k, v in kwargs.items():
                if k in ("created_at", "updated_at"):
                    self.__dict__[k] = datetime.\
                                       strptime(v, "%Y-%m-%dT%H:%M:%S.%f")
                elif k == "__class__":
                    continue
                else:
                    self.__dict__[k] = v

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        # storage.new(self)

    def __str__(self):
        """
        Prints the string representation of the object
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """
        Updates when the object is modified
        """
        from models import storage
        self.updated_at = datetime.datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """
        Returns a dictionary representation of the object
        """
        dict = {}
        dict["__class__"] = self.__class__.__name__

        for k, v in self.__dict__.items():
            if isinstance(v, datetime):
                v = v.isoformat()
                dict[k] = v

            dict[k] = v

        if "_sa_instance_state" in dict.keys():
            del dict["_sa_instance_state"]

        return dict

    # def to_dict(self):
    #     dictionary = {}
    #     dictionary.update(self.__dict__)
    #     dictionary.update({'__class__':
    #                       (str(type(self)).split('.')[-1]).split('\'')[0]})
    #     dictionary['created_at'] = self.created_at.isoformat()
    #     dictionary['updated_at'] = self.updated_at.isoformat()

    #     if "_sa_instance_state" in dictionary.keys():
    #         del dictionary["_sa_instance_state"]

    #     return dictionary
