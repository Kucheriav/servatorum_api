from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Boolean, Enum
from sqlalchemy.orm import validates, relationship
from app.models.sphere_model import user_spheres
from app.database import Base
from app.config import settings
import re
import hashlib
import binascii
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    # логина как такового нет
    # login = Column(String, nullable=False)
    _password = Column(String, nullable=False)
    first_name = Column(String)
    surname = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    gender = Column(String)
    city = Column(String)
    address = Column(String)
    email = Column(String, unique=True)
    phone = Column(String, unique=True)
    profile_picture = Column(String)
    role = Column(Enum('helping', 'getting help', name="user_role_enum"), nullable=False)
    spheres = relationship("Sphere", secondary=user_spheres, back_populates="users")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Проверяем наличие либо email, либо пароля
        if not any([self.email, self.phone]):
            raise ValueError("Необходимо передать хотя бы email или номер телефона.")

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

class UserMeta(Base):
    __tablename__ = "user_meta"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    prefer_help = Column(String)
    achieves = Column(String)


class UserToken(Base):
    __tablename__ = "user_tokens"
    id = Column(Integer, primary_key=True)
    access_token = Column(String)
    refresh_token = Column(String)
    valid_before = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))


class UserEntityRelation(Base):
    __tablename__ = "user_entity_relations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    entity_id = Column(Integer)  # id компании или фонда
    entity_type = Column(String(50))  # "company" или "foundation"


class UserVerificationCode(Base):
    __tablename__ = "user_verification_codes"
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, index=True, nullable=False)
    code = Column(String, nullable=False)
    is_used = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)