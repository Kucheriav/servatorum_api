from pydantic import BaseModel, field_validator
from typing import Dict, Any
import re


class LegalEntityCreate(BaseModel):
    name: str
    description: str
    logo: str
    photo: str
    inn: str
    bik: str
    cor_account: str
    address: str
    address_reg: str
    phone: str
    phone_helpdesk: str
    entity_type: str

    @staticmethod
    @field_validator('phone', 'phone_helpdesk')
    def phone_format(v):
        if not re.match(r'^7\d{9}$', v):
            raise ValueError('Неправильный формат телефона')
        return v

    @staticmethod
    @field_validator('bik')
    def bik_format(v):
        if not re.match(r'^[0-9]{9}$', v):
            raise ValueError('Неправильный формат БИК')
        return v

    @staticmethod
    @field_validator('inn')
    def inn_format(v):
        if not re.match(r'^[0-9]{10}$', v):
            raise ValueError('Неправильный формат ИНН')
        return v

    @staticmethod
    @field_validator('cor_account')
    def cor_account_format(v):
        if not re.match(r'^[0-9]{20}$', v):
            raise ValueError('Неправильный формат корреспондентского счета')
        return v

    @staticmethod
    @field_validator('entity_type')
    def entity_type_format(v):
        if v not in ['company', 'foundation']:
            raise ValueError('Неправильный тип юридического лица')
        return v


class LegalEntityPatch(BaseModel):
    legal_entity_id: int
    params: Dict[str, Any]

    @staticmethod
    @field_validator('params')
    def validate_individual_fields(v):
        for key in v:
            if key == 'phone' or key == 'phone_helpdesk':
                LegalEntityCreate.phone_format(v[key])
            elif key == 'bik':
                LegalEntityCreate.bik_format(v[key])
            elif key == 'inn':
                LegalEntityCreate.inn_format(v[key])
            elif key == 'cor_account':
                LegalEntityCreate.cor_account_format(v[key])
            elif key == 'entity_type':
                LegalEntityCreate.entity_type_format(v[key])
        return v
