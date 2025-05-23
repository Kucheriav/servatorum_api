from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Float
from sqlalchemy.orm import validates
from app.database import Base
from app.config import settings
import re
import hashlib
import binascii


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    _password = Column(String, nullable=False)
    first_name = Column(String)
    surname = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    gender = Column(String)
    city = Column(String)
    address = Column(String)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    profile_picture = Column(String)

    # fundraisings = relationship("Fundraising", back_populates="owner")
    # complaints = relationship("Complaint", back_populates="user")

    @property
    def password(self):
        raise AttributeError("Нельзя напрямую получить значение пароля")

    def set_password(self, password):
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), settings.get_salt().encode('utf-8'), 100000)
        self._password = binascii.hexlify(pwdhash).decode('utf-8')

    def verify_password(self, password):
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), settings.get_salt().encode('utf-8'), 100000)
        return self._password == binascii.hexlify(pwdhash).decode('utf-8')

    @validates('phone_number')
    def validate_phone_number(self, phone_number):
        pattern = r'^\+\d{11}$'
        if not re.match(pattern, phone_number):
            raise ValueError(f"Неверный формат номера телефона: {phone_number}. Ожидается формат: +71234567890")
        return phone_number


class UserCompanyRelation(Base):
    __tablename__ = "user_company_relations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    company_id = Column(Integer, ForeignKey('legalentitys.id'))


class UserMeta(Base):
    __tablename__ = "user_meta"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    prefer_help = Column(String)
    achieves = Column(String)


class UserDonation(Base):
    __tablename__ = "user_donations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    fundraising_id = Column(Integer, ForeignKey('fundraisings.id'))
    amount = Column(Float)
    date = Column(DateTime)


class UserToken(Base):
    __tablename__ = "user_tokens"
    id = Column(Integer, primary_key=True)
    token = Column(String)
    refresh_token = Column(String)
    valid_before = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))