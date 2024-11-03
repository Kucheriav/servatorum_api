from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy.sql import func
from .database import Base
import re, os, hashlib, binascii


fund_charity_sphere_association = Table(
    'fund_charity_sphere',
    Base.metadata,
    Column('fund_id', Integer, ForeignKey('funds.id'), primary_key=True),
    Column('charity_sphere_id', Integer, ForeignKey('charity_sphere.id'), primary_key=True)
)


class CharitySphere(Base):
    __tablename__ = 'charity_sphere'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    funds = relationship("Fund", secondary=fund_charity_sphere_association, back_populates="charity_spheres")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    profile_picture = Column(String)
    _pin_code = Column(String, nullable=False)
    _pin_code_salt = Column(String, nullable=False)
    registration_date = Column(DateTime, default=func.now())
    fundraisings = relationship("Fundraising", back_populates="owner")
    complaints = relationship("Complaint", back_populates="user")


    @property
    def pin_code(self):
        raise AttributeError("Нельзя напрямую получить значение pin_code")

    @property
    def pin_code_salt(self):
        raise AttributeError("Нельзя напрямую получить значение pin_code_salt")

    @validates('phone_number')
    def validate_phone_number(self, phone_number):
        pattern = r'^\+\d{11}$'
        if not re.match(pattern, phone_number):
            raise ValueError(f"Неверный формат номера телефона: {phone_number}. Ожидается формат: +71234567890")
        return phone_number

    def set_pin_code(self, pin_code):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', pin_code.encode('utf-8'), salt, 100000)
        # Хранение хеш-значения и соли
        self._pin_code = binascii.hexlify(pwdhash).decode('utf-8')
        self._pin_code_salt = salt.decode('utf-8')

    def verify_pin_code(self, pin_code):
        # Получение хеш-значения и соли из базы данных
        stored_pin_code = self._pin_code
        stored_pin_code_salt = self._pin_code_salt.encode('ascii')
        # Хеширование введенного пин-кода
        pwdhash = hashlib.pbkdf2_hmac('sha512', pin_code.encode('utf-8'), stored_pin_code_salt, 100000)
        return stored_pin_code == binascii.hexlify(pwdhash).decode('utf-8')

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



class Fund(Base):
    __tablename__ = "funds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    admin_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    inn = Column(String, nullable=False)
    kpp = Column(String, nullable=False)
    address = Column(String, nullable=False)
    profile_picture = Column(String)
    phone = Column(String, nullable=False)
    email = Column(String)
    website = Column(String)
    fundraisings = relationship("Fundraising", back_populates="fund")
    posts = relationship("Post", back_populates="fund")
    accounts = relationship("Account", back_populates="fund")
    charity_spheres = relationship("CharitySphere", secondary=fund_charity_sphere_association, back_populates="funds")

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey('funds.id'), nullable=False)
    name = Column(String, nullable=False)
    bic = Column(String, nullable=False)
    ks_number = Column(String, nullable=False)
    account_number = Column(String, nullable=False)
    fund = relationship("Fund", back_populates="accounts")

class Fundraising(Base):
    __tablename__ = "fundraising"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    status = Column(Enum("draft", "published", "completed", name="status_enum"))

    owner_id = Column(Integer, ForeignKey('users.id'))
    fund_id = Column(Integer, ForeignKey('funds.id'))

    owner = relationship("User", back_populates="fundraisings")
    fund = relationship("Fund", back_populates="fundraisings")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)

    fund_id = Column(Integer, ForeignKey('funds.id'))
    fund = relationship("Fund", back_populates="posts")


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="complaints")