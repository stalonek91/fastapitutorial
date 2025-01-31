from .database import base

from sqlalchemy.sql.expression import text
from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime
from sqlalchemy.sql.sqltypes import TIMESTAMP


class User(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Post(base):
    __tablename__ = 'class_post'

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True, nullable=False)
    created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))



