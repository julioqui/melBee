from ctypes.wintypes import BYTE
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import relationship
from database.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Template(Base):
    __tablename__ = "template"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    thumbnail = Column(String, nullable=False)
    body = Column(String, nullable=False)

# TODO: Migrate other tables
# class Email_Sent(Base):
#     __tablename__ = "email_sent"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("user.id"),  index=True)
