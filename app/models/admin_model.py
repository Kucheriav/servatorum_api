from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import validates
from app.database import Base
from app.config import settings
import re
import hashlib
import binascii


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False,unique=True)
    is_superadmin = Column(Boolean, default=False)
    profile_picture = Column(String)


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


class AdminToken(Base):
    __tablename__ = "admin_tokens"
    id = Column(Integer, primary_key=True)
    token = Column(String)
    refresh_token = Column(String)
    valid_before = Column(DateTime)
    admin_id = Column(Integer, ForeignKey('admins.id'))


class AdminVerificationCode(Base):
    __tablename__ = "admin_verification_codes"
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, index=True, nullable=False)
    code = Column(String, nullable=False)
    is_used = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)