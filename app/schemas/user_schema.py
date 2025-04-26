from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, Dict, Any
from datetime import date
import re


# помечаем необязательные first_name: Optional[str] = None, чтобы вместо непереданных появилось значение по умлочанию
class UserCreate(BaseModel):
    login: str
    password: str
    first_name: Optional[str] = None
    surname: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    email: EmailStr
    phone: str
    profile_picture: Optional[str] = None


    @staticmethod
    @field_validator('phone')
    def phone_format(v):
        if not re.match(r'^7\d{9}$', v):
            raise ValueError('Неправильный формат телефона')
        return v

    @staticmethod
    @field_validator('password')
    def password_min_length(v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserResponse(BaseModel):
    user_id: int
    login: str
    email: EmailStr
    first_name: Optional[str] = None
    surname: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    city: Optional[str] = None


class UserPatch(BaseModel):
    user_id: int
    params: Dict[str, Any]

    @staticmethod
    @field_validator('params')
    def validate_individual_fields(v):
        for key in v:
            if key == 'phone':
                UserCreate.phone_format(v[key])
            elif key == 'password':
                UserCreate.password_min_length(v[key])
        return v