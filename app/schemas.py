from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List

class UserBase(BaseModel):
    first_name: str
    phone: str

class User(UserBase):
    id: int
    profile_picture: Optional[str]
    registration_date: datetime
    collections: List[int] = []
    complaints: List[int] = []

    class Config:
        orm_mode = True

class RecipientBase(BaseModel):
    last_name: str
    address: str
    birth_date: date
    email: str
    gender: str

class Recipient(RecipientBase):
    patronymic: Optional[str]

class RecipientFull(User, Recipient):
    pass

class Donor(User):
    pass

class CharitySphereBase(BaseModel):
    name: str

class CharitySphere(CharitySphereBase):
    id: int
    funds: List['Fund'] = []

    class Config:
        orm_mode = True

class FundBase(BaseModel):
    name: str
    admin_user_id: int
    inn: str
    kpp: str
    address: str
    phone: str
    email: Optional[str]
    website: Optional[str]

class Fund(FundBase):
    id: int
    profile_picture: Optional[str]
    charity_spheres: List[CharitySphere] = []
    fundraisings: List['Fundraising'] = []
    posts: List['Post'] = []
    accounts: List['Account'] = []

    class Config:
        orm_mode = True

class AccountBase(BaseModel):
    name: str
    bic: str
    ks_number: str
    account_number: str

class Account(AccountBase):
    id: int
    fund_id: int
    fund: 'Fund'

    class Config:
        orm_mode = True

class CollectionBase(BaseModel):
    title: str
    content: str
    status: str


class CollectionCreate(CollectionBase):
    pass


class Collection(CollectionBase):
    id: int

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int

    class Config:
        orm_mode = True


class ComplaintBase(BaseModel):
    content: str


class ComplaintCreate(ComplaintBase):
    pass


class Complaint(ComplaintBase):
    id: int

    class Config:
        orm_mode = True