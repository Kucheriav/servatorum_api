from pydantic import BaseModel, field_validator, EmailStr
from typing import Dict, Any, Optional
import re
import logging

logger = logging.getLogger("pydantic_validation")

class LegalEntityCreate(BaseModel):
    administrator_name: str
    administrator_surname: str
    administrator_lastname: str
    name: str
    description: str
    address: str
    phone: str
    email: EmailStr
    site: str
    logo: Optional[str] = None


    @field_validator('phone')
    @staticmethod
    def phone_format(v):
        if not re.match(r'^7\d{10}$', v):
            raise ValueError('Неправильный формат телефона')
        return v

class LegalEntityResponse(BaseModel):
    id: int
    administrator_name: str
    administrator_surname: str
    administrator_lastname: str
    name: str
    description: str
    address: str
    phone: str
    email: EmailStr
    site: str
    logo: Optional[str] = None

class LegalEntityPatch(BaseModel):
    params: Dict[str, Any]

    @field_validator('params')
    @staticmethod
    def validate_individual_fields(v):
        for key in v:
            if key == 'phone':
                LegalEntityCreate.phone_format(v[key])
        return v

class LegalEntityAccountDetailsCreate(BaseModel):
    inn: str
    kpp: str
    account_name: str
    bank_account: str
    cor_account: str
    bik: str

    @field_validator('inn')
    @staticmethod
    def inn_format(v):
        if not re.match(r'^[0-9]{10}$', v):
            raise ValueError('Неправильный формат ИНН')
        return v

    @field_validator('kpp')
    @staticmethod
    def kpp_format(v):
        if not re.match(r'^[0-9]{9}$', v):
            raise ValueError('Неправильный формат КПП')
        return v

    @field_validator('bank_account')
    @staticmethod
    def bank_account_format(v):
        if not re.match(r'^[0-9]{20}$', v):
            raise ValueError('Неправильный формат расчётного счёта')
        return v

    @field_validator('cor_account')
    @staticmethod
    def cor_account_format(v):
        if not re.match(r'^[0-9]{20}$', v):
            raise ValueError('Неправильный формат корреспондентского счета')
        return v

    @field_validator('bik')
    @staticmethod
    def bik_format(v):
        if not re.match(r'^[0-9]{9}$', v):
            raise ValueError('Неправильный формат БИК')
        return v


class LegalEntityAccountDetailsPatch(BaseModel):
    id: Optional[int] = None
    inn: Optional[str] = None
    kpp: Optional[str] = None
    account_name: Optional[str] = None
    bank_account: Optional[str] = None
    cor_account: Optional[str] = None
    bik: Optional[str] = None

    @field_validator('inn')
    @staticmethod
    def inn_format(v):
        if v is not None and not re.match(r'^[0-9]{10}$', v):
            raise ValueError('Неправильный формат ИНН')
        return v

    @field_validator('kpp')
    @staticmethod
    def kpp_format(v):
        if v is not None and not re.match(r'^[0-9]{9}$', v):
            raise ValueError('Неправильный формат КПП')
        return v

    @field_validator('bank_account')
    @staticmethod
    def bank_account_format(v):
        if v is not None and not re.match(r'^[0-9]{20}$', v):
            raise ValueError('Неправильный формат расчётного счёта')
        return v

    @field_validator('cor_account')
    @staticmethod
    def cor_account_format(v):
        if v is not None and not re.match(r'^[0-9]{20}$', v):
            raise ValueError('Неправильный формат корреспондентского счета')
        return v

    @field_validator('bik')
    @staticmethod
    def bik_format(v):
        if v is not None and not re.match(r'^[0-9]{9}$', v):
            raise ValueError('Неправильный формат БИК')
        return v