# from pydantic import BaseModel, field_validator
# from typing import Dict, Any
# import re
# import logging
#
#
# logger = logging.getLogger("pydantic_validation")
#
# class LegalEntityCreate(BaseModel):
#     name: str
#     description: str
#     logo: str
#     photo: str | None = None
#     inn: str #= Field(..., description="INN must be exactly 10 digits.", min_length=10, max_length=10, pattern=r"^\d{10}$")
#     bik: str #= Field(..., description="BIK must be exactly 9 digits.", min_length=9, max_length=9, pattern=r"^\d{9}$")
#     cor_account: str #= Field(..., description="Correspondent Account must be exactly 20 digits.", min_length=20, max_length=20, pattern=r"^\d{20}$")
#     address: str
#     address_reg: str
#     phone: str #= Field(..., description="Phone must follow the format '7XXXXXXXXXX'.", min_length=11, max_length=11, pattern=r"^7\d{10}$")
#     phone_helpdesk: str #= Field(..., description="Helpdesk Phone must follow the format '7XXXXXXXXXX'.", min_length=11, max_length=11, pattern=r"^7\d{10}$")
#
#     @field_validator('phone', 'phone_helpdesk')
#     @staticmethod
#     def phone_format(v):
#         if not re.match(r'^7\d{10}$', v):
#             raise ValueError('Неправильный формат телефона')
#         return v
#
#     @field_validator('bik')
#     @staticmethod
#     def bik_format(v):
#         if not re.match(r'^[0-9]{9}$', v):
#             raise ValueError('Неправильный формат БИК')
#         return v
#
#     @field_validator('inn')
#     @staticmethod
#     def inn_format(v):
#         if not re.match(r'^[0-9]{10}$', v):
#             raise ValueError('Неправильный формат ИНН')
#         return v
#
#     @field_validator('cor_account')
#     @staticmethod
#     def cor_account_format(v):
#         if not re.match(r'^[0-9]{20}$', v):
#             raise ValueError('Неправильный формат корреспондентского счета')
#         return v
#
#
# class LegalEntityResponse(BaseModel):
#     id: int
#     name: str
#     description: str
#     logo: str
#     #photo: str
#     inn: str
#     bik: str
#     cor_account: str
#     address: str
#     address_reg: str
#     phone: str
#     phone_helpdesk: str
#
#
# class LegalEntityPatch(BaseModel):
#     params: Dict[str, Any]
#
#     @field_validator('params')
#     @staticmethod
#     def validate_individual_fields(v):
#         for key in v:
#             if key == 'phone' or key == 'phone_helpdesk':
#                 LegalEntityCreate.phone_format(v[key])
#             elif key == 'bik':
#                 LegalEntityCreate.bik_format(v[key])
#             elif key == 'inn':
#                 LegalEntityCreate.inn_format(v[key])
#             elif key == 'cor_account':
#                 LegalEntityCreate.cor_account_format(v[key])
#         return v

from pydantic import BaseModel, field_validator
from typing import Dict, Any, Optional
import re
import logging

logger = logging.getLogger("pydantic_validation")

class LegalEntityCreate(BaseModel):
    name: str
    description: str
    logo: str
    photo: Optional[str] = None
    address: str
    address_reg: str
    phone: str
    phone_helpdesk: str

    @field_validator('phone', 'phone_helpdesk')
    @staticmethod
    def phone_format(v):
        if not re.match(r'^7\d{10}$', v):
            raise ValueError('Неправильный формат телефона')
        return v

class LegalEntityResponse(BaseModel):
    id: int
    name: str
    description: str
    logo: str
    address: str
    address_reg: str
    phone: str
    phone_helpdesk: str

class LegalEntityPatch(BaseModel):
    params: Dict[str, Any]

    @field_validator('params')
    @staticmethod
    def validate_individual_fields(v):
        for key in v:
            if key == 'phone' or key == 'phone_helpdesk':
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