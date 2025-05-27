from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional, List, Literal, Dict, Any
import enum

class WalletCreate(BaseModel):
    owner_type: Literal['user', 'company', 'foundation'] = Field(..., description="Тип владельца кошелька")
    owner_id: int = Field(..., gt=0, description="ID владельца кошелька")
    balance: float = Field(0.0, ge=0, description="Начальный баланс (обычно 0, не может быть отрицательным)")

    @field_validator('owner_type')
    @staticmethod
    def owner_type_valid(v):
        if v not in ['user', 'company', 'foundation']:
            raise ValidationError("owner_type должен быть 'user', 'company' или 'foundation'")
        return v

class WalletResponse(BaseModel):
    wallet_id: int
    owner_type: str
    owner_id: int
    balance: float

    class Config:
        orm_mode = True

class WalletPatch(BaseModel):
    params: Dict[str, Any]

    @field_validator('params')
    @staticmethod
    def validate_individual_fields(v):
        for key in v:
            if key == 'balance':
                if v[key] < 0:
                    raise ValidationError("Баланс не может быть отрицательным")
            if key == 'owner_type':
                WalletCreate.owner_type_valid(v[key])
        return v