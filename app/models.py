from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy.sql import func
from .database import Base
import re, os, hashlib, binascii





class Fundraising(Base):
    __tablename__ = "fundraising"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    status = Column(Enum("draft", "published", "completed", name="status_enum"))
    owner_id = Column(Integer, ForeignKey('users.id'))
    fund_id = Column(Integer, ForeignKey('funds.id'))

    # owner = relationship("User", back_populates="fundraisings")
    # fund = relationship("Fund", back_populates="fundraisings")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    fund_id = Column(Integer, ForeignKey('funds.id'))

    # fund = relationship("Fund", back_populates="posts")


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    # user = relationship("User", back_populates="complaints")