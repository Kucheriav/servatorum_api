import logging

from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, Literal, Optional

logger = logging.getLogger("pydantic_validation")

class LegalEntityCreate(BaseModel):
    name: str
    description: str
    logo: str
    photo: Optional[str] = None
    inn: str = Field(..., description="INN must be exactly 10 digits.", min_length=10, max_length=10, pattern=r"^\d{10}$")
    bik: str = Field(..., description="BIK must be exactly 9 digits.", min_length=9, max_length=9, pattern=r"^\d{9}$")
    cor_account: str = Field(..., description="Correspondent Account must be exactly 20 digits.", min_length=20, max_length=20, pattern=r"^\d{20}$")
    address: str
    address_reg: str
    phone: str = Field(..., description="Phone must follow the format '7XXXXXXXXXX'.", min_length=11, max_length=11, pattern=r"^7\d{10}$")
    phone_helpdesk: str = Field(..., description="Helpdesk Phone must follow the format '7XXXXXXXXXX'.", min_length=11, max_length=11, pattern=r"^7\d{10}$")
    entity_type: Literal['company', 'foundation'] = Field(..., description="Entity type must be 'company' or 'foundation'.")

    # it is never called i dont know why
    # @classmethod
    # @field_validator('*', mode='before')
    # def log_field_validation(cls, value, field):
    #     print(1)
    #     logger.info(f"Validating field '{field.name}' with value '{value}'")
    #     return value
    #
    # @classmethod
    # @field_validator('entity_type', mode='before')
    # def validate_entity_type(cls, v):
    #     print(2)
    #     valid_types = ['company', 'foundation']
    #     if v not in valid_types:
    #         raise ValueError(f"Invalid entity type: {v}. Must be one of {valid_types}.")
    #     return v

class LegalEntityResponse(BaseModel):
    id: int
    name: str
    description: str
    logo: str
    #photo: str
    inn: str
    bik: str
    cor_account: str
    address: str
    address_reg: str
    phone: str
    phone_helpdesk: str
    entity_type: str

class LegalEntityPatch(BaseModel):
    name: str
    description: str
    logo: str
    photo: Optional[str] = None
    inn: str = Field(..., description="INN must be exactly 10 digits.", min_length=10, max_length=10, pattern=r"^\d{10}$")
    bik: str = Field(..., description="BIK must be exactly 9 digits.", min_length=9, max_length=9, pattern=r"^\d{9}$")
    cor_account: str = Field(..., description="Correspondent Account must be exactly 20 digits.", min_length=20, max_length=20, pattern=r"^\d{20}$")
    address: str
    address_reg: str
    phone: str = Field(..., description="Phone must follow the format '7XXXXXXXXXX'.", min_length=11, max_length=11, pattern=r"^7\d{10}$")
    phone_helpdesk: str = Field(..., description="Helpdesk Phone must follow the format '7XXXXXXXXXX'.", min_length=11, max_length=11, pattern=r"^7\d{10}$")
    entity_type: Literal['company', 'foundation'] = Field(..., description="Entity type must be 'company' or 'foundation'.")
