import logging

from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any

logger = logging.getLogger("pydantic_validation")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class LegalEntityCreate(BaseModel):
    name: str
    description: str
    logo: str
    photo: str
    inn: str = Field(..., description="INN must be exactly 10 digits.", min_length=10, max_length=10, pattern=r"^\d{10}$")
    bik: str = Field(..., description="BIK must be exactly 9 digits.", min_length=9, max_length=9, pattern=r"^\d{9}$")
    cor_account: str = Field(..., description="Correspondent Account must be exactly 20 digits.", min_length=20, max_length=20, pattern=r"^\d{20}$")
    address: str
    address_reg: str
    phone: str = Field(..., description="Phone must follow the format '7XXXXXXXXXX'.", min_length=11, max_length=11, pattern=r"^7\d{9}$")
    phone_helpdesk: str = Field(..., description="Helpdesk Phone must follow the format '7XXXXXXXXXX'.", min_length=11, max_length=11, pattern=r"^7\d{9}$")
    entity_type: str = Field(..., description="Entity type must be 'company' or 'foundation'.")


    @classmethod
    @field_validator('entity_type', mode='before')
    def validate_entity_type(cls, v):
        valid_types = ['company', 'foundation']
        if v not in valid_types:
            raise ValueError(f"Invalid entity type: {v}. Must be one of {valid_types}.")
        return v

# class LegalEntityCreate(BaseModel):
#     name: str
#     description: str
#     logo: str
#     photo: str
#     inn: str
#     bik: str
#     cor_account: str
#     address: str
#     address_reg: str
#     phone: str
#     phone_helpdesk: str
#     entity_type: str
#
#     @staticmethod
#     @field_validator('phone', 'phone_helpdesk')
#     def phone_format(v):
#         if not re.match(r'^7\d{9}$', v):
#             raise ValueError('Неправильный формат телефона')
#         return v
#
#     @staticmethod
#     @field_validator('bik')
#     def bik_format(v):
#         if not re.match(r'^[0-9]{9}$', v):
#             raise ValueError('Неправильный формат БИК')
#         return v
#
#     @staticmethod
#     @field_validator('inn')
#     def inn_format(v):
#         if not re.match(r'^[0-9]{10}$', v):
#             raise ValueError('Неправильный формат ИНН')
#         return v
#
#     @staticmethod
#     @field_validator('cor_account')
#     def cor_account_format(v):
#         if not re.match(r'^[0-9]{20}$', v):
#             raise ValueError('Неправильный формат корреспондентского счета')
#         return v
#
#     @staticmethod
#     @field_validator('entity_type')
#     def entity_type_format(v):
#         if v not in ['company', 'foundation']:
#             raise ValueError('Неправильный тип юридического лица')
#         return v

class LegalEntityResponse(BaseModel):
    legal_entity_id: int
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

class LegalEntityPatch(BaseModel):
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
