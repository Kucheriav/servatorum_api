from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy.sql import func
from app.database import Base
import re
import os
import hashlib
import binascii


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    _password = Column(String, nullable=False)
    _password_code_salt = Column(String, nullable=False)
    first_name = Column(String)
    surname = Column(String)
    last_name = Column(String)
    date_of_birth = Column(DateTime)
    gender = Column(String)
    city = Column(String)
    _email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)
    profile_picture = Column(String)
    registration_date = Column(DateTime, default=func.now())

    # fundraisings = relationship("Fundraising", back_populates="owner")
    # complaints = relationship("Complaint", back_populates="user")

    @property
    def password(self):
        raise AttributeError("Нельзя напрямую получить значение пароля")

    def set_password(self, password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
        self._password = binascii.hexlify(pwdhash).decode('utf-8')
        self._password_salt = salt.decode('utf-8')

    def verify_password(self, password):
        stored_password = self._password
        stored_password_salt = self._password_salt.encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), stored_password_salt, 100000)
        return stored_password == binascii.hexlify(pwdhash).decode('utf-8')

    @validates('phone_number')
    def validate_phone_number(self, phone_number):
        pattern = r'^\+\d{11}$'
        if not re.match(pattern, phone_number):
            raise ValueError(f"Неверный формат номера телефона: {phone_number}. Ожидается формат: +71234567890")
        return phone_number


class Recipient(User):
    __tablename__ = 'recipients'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    last_name = Column(String, nullable=False)
    patronymic = Column(String)
    address = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    email = Column(String, nullable=False, unique=True)
    gender = Column(String, nullable=False)

    @validates('gender')
    def validate_gender(self, key, value):
        if value not in ['мужской', 'женский']:
            raise ValueError('Пол должен быть либо "мужской", либо "женский"')
        return value


class Donor(User):
    __tablename__ = 'donors'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)

