from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    login: str
    email: EmailStr
    first_name: Optional[str] = None
    surname: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    city: Optional[str] = None
    phone: str
    password: str

