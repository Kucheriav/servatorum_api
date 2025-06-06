from pydantic import BaseModel, field_validator
import re

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