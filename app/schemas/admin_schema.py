from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, Dict, Any
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


class AdminCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    phone: str
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


class AdminResponse(BaseModel):
    id: int
    username: str
    password: str
    email: EmailStr
    phone: str
    profile_picture: Optional[str] = None

class AuthResponse(BaseModel):
    user: Optional[AdminResponse] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    status: str = "ok"
    is_new: bool = False

class AdminPatch(BaseModel):
    params: Dict[str, Any]


    @field_validator('params')
    @staticmethod
    def validate_individual_fields(v):
        for key in v:
            if key == 'phone':
                AdminCreate.phone_format(v[key])
            elif key == 'password':
                AdminCreate.password_min_length(v[key])
        return v