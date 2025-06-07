from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional, Dict, Any
import datetime
import re

import logging

logger = logging.getLogger(__name__)

class RequestCodeSchema(BaseModel):
    phone: str

    @field_validator("phone")
    @classmethod
    def phone_format(cls, v):
        # Ожидаем 7XXXXXXXXXX или +7XXXXXXXXXX
        if not re.match(r"^7\d{10}$", v) and not re.match(r"^\+7\d{10}$", v):
            raise ValueError("Номер должен быть в формате 7XXXXXXXXXX или +7XXXXXXXXXX")
        return v.lstrip("+")

class VerifyCodeSchema(BaseModel):
    phone: str
    code: str

    @field_validator("phone")
    @classmethod
    def phone_format(cls, v):
        if not re.match(r"^7\d{10}$", v) and not re.match(r"^\+7\d{10}$", v):
            raise ValueError("Номер должен быть в формате 7XXXXXXXXXX или +7XXXXXXXXXX")
        return v.lstrip("+")

class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    # login: str
    password: str
    first_name: Optional[str] = None
    surname: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[datetime.date] = None
    gender: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    profile_picture: Optional[str] = None


    @field_validator('phone')
    @classmethod
    def phone_format(cls, v):
        logger.info(f"Validating phone: {v}")
        if not re.match(r'^7\d{10}$', v):
            raise ValueError('Phone number must be "71234567890" like')
        return v


    @field_validator('password')
    @classmethod
    def password_min_length(cls, v):
        logger.info(f"Validating password: {v}")
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

    @model_validator(mode='after')
    def check_email_or_phone(self):
        if not self.phone and not self.email:
            raise ValueError("Необходимо задать хотя бы одно из полей: email или phone.")
        return self

class UserResponse(BaseModel):
    id: int
    login: str
    email: EmailStr
    phone: str
    first_name: Optional[str] = None
    surname: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[datetime.date] = None
    gender: Optional[str] = None
    city: Optional[str] = None


class UserPatch(BaseModel):
    params: Dict[str, Any]


    @field_validator('params')
    @staticmethod
    def validate_individual_fields(v):
        for key in v:
            if key == 'phone':
                UserCreate.phone_format(v[key])
            elif key == 'password':
                UserCreate.password_min_length(v[key])
            elif key == 'date_of_birth':
                try:
                    temp = datetime.datetime.strptime(v[key], '%Y-%m-%d').date()
                    # parsed_date = datetime.strptime(v[key], '%Y-%m-%d').date()
                    v[key] = temp
                except ValueError:
                    raise ValueError(f"Invalid date format for key '{key}'. Expected format: YYYY-MM-DD")
            elif key == 'balance':
                raise ValueError(f"Can't patch balance")
        return v