#!/usr/bin/python3
"""DataBase storage module"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.base_model import BaseModel, Base
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """class definition for dbstorage"""
    __engine = None
    __session = None

    def __init__(self):
        """initialize dbstorage class"""
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        conn = f"mysql+mysqldb://{user}:{passwd}@{host}/{db}"

        self.__engine = create_engine(conn, pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        query on the current database session
        all objects depending of the class name
        """
        classes = [User, State, City, Amenity, Place, Review]
        dictionary = {}

        if cls is None:
            for item in classes:
                query = self.__session.query(item).all()
                for obj in query:
                    obj_key = f"{obj.__class__.__name__}.{obj.id}"
                    dictionary[obj_key] = obj
        else:
            query = self.__session.query(cls).all()
            for obj in query:
                obj_key = f"{obj.__class__.__name__}.{obj.id}"
                dictionary[obj_key] = obj

        return dictionary

    # def all(self, cls=None):
    #     classes = [User, State, City, Amenity, Place, Review]
    #     dictionary = {}

    #     if cls is None:
    #         for item in classes:
    #             query = self.__session.query(item).all()
    #             for obj in query:
    #                 obj_class = obj.__class__.__name__
    #                 obj_id = obj.id
    #                 obj_key = str(obj_class)+'.'+str(obj_id)

    #                 dictionary[obj_key] = obj

    #         return dictionary
    #     else:
    #         query = self.__session.query(cls).all()
    #         for obj in query:
    #             obj_class= obj.__class__.__name__
    #             obj_id = obj.id
    #             obj_key = str(obj_class)+'.'+str(obj_id)

    #             dictionary[obj_key] = obj
    #         return dictionary

    def new(self, obj):
        """
        add the object to the current database session
        """
        self.__session.add(obj).to_dict()

    def save(self):
        """
        commit all changes of the current database session
        """
        self.__session.commit().to_dict()

    def delete(self, obj=None):
        """
        delete from the current database session
        """
        self.__session.delete(obj)

    def reload(self):
        """"create all tables in the database"""
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)

        self.__session = Session()
