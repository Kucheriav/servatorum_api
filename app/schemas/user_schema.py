from pydantic import BaseModel, EmailStr, field_validator, model_validator, Field
from typing import Optional, Dict, Any, List, Literal
import datetime
import re

import logging

logger = logging.getLogger(__name__)

class RequestCodeSchema(BaseModel):
    phone: str

    @field_validator("phone")
    @classmethod
    def phone_format(cls, v):
        logger.info(f"Validating phone: {v}")
        if not re.match(r'^7\d{10}$', v):
            raise ValueError('Phone number must be "71234567890" like')
        return v

class VerifyCodeSchema(BaseModel):
    phone: str
    code: str

    @field_validator("phone")
    @classmethod
    def phone_format(cls, v):
        logger.info(f"Validating phone: {v}")
        if not re.match(r'^7\d{10}$', v):
            raise ValueError('Phone number must be "71234567890" like')
        return v

class NewUserResponse(BaseModel):
    status: str
    is_new: bool

class UserCreate(BaseModel):
    # login: str
    # password: str
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
    role: Literal['helping', 'getting help'] = Field(..., description="Что пользователь хочет")
    spheres: Optional[List[int]] = None


    @field_validator('phone')
    @classmethod
    def phone_format(cls, v):
        logger.info(f"Validating phone: {v}")
        if not re.match(r'^7\d{10}$', v):
            raise ValueError('Phone number must be "71234567890" like')
        return v


    # @field_validator('password')
    # @classmethod
    # def password_min_length(cls, v):
    #     logger.info(f"Validating password: {v}")
    #     if len(v) < 8:
    #         raise ValueError('Password must be at least 8 characters long')
    #     return v

    @model_validator(mode='after')
    def check_email_or_phone(self):
        if not self.phone and not self.email:
            raise ValueError("Необходимо задать хотя бы одно из полей: email или phone.")
        return self

class UserResponse(BaseModel):
    id: int
    first_name: Optional[str] = None
    surname: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[datetime.date] = None
    gender: Optional[str] = None
    city: Optional[str] = None
    email: EmailStr
    phone: str
    role: str
    spheres: Optional[List[int]]

class AuthResponse(BaseModel):
    user: Optional[UserResponse] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    status: str = "ok"
    is_new: bool = False

class UserPatch(BaseModel):
    params: Dict[str, Any]


    @field_validator('params')
    @staticmethod
    def validate_individual_fields(v):
        for key in v:
            if key == 'phone':
                UserCreate.phone_format(v[key])
            # elif key == 'password':
            #     UserCreate.password_min_length(v[key])
            elif key == 'date_of_birth':
                try:
                    temp = datetime.datetime.strptime(v[key], '%Y-%m-%d').date()
                    v[key] = temp
                except ValueError:
                    raise ValueError(f"Invalid date format for key '{key}'. Expected format: YYYY-MM-DD")
            elif key == 'balance':
                raise ValueError(f"Can't patch balance")
        return v