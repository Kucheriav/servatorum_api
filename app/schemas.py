from pydantic import BaseModel
from typing import List, Optional


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    collections: List[int] = []
    complaints: List[int] = []

    class Config:
        orm_mode = True


class FundBase(BaseModel):
    name: str


class FundCreate(FundBase):
    pass


class Fund(FundBase):
    id: int
    collections: List[int] = []
    posts: List[int] = []

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