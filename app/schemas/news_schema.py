from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List, Dict, Any


class NewsCreate(BaseModel):
    title: str
    description: str
    publication_date: datetime
    photo: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    @field_validator('title')
    def title_len(v):
        if not(0 < v < 256):
            raise ValueError('Incorrect field length. Must be [1 .. 255]')
        return v

    @staticmethod
    @field_validator('description')
    def description_len(v):
        if not(0 < v < 1001):
            raise ValueError('Incorrect field length. Must be [1 .. 1000]')
        return v

class NewsResponse(BaseModel):
    news_id: int
    title: str
    description: str
    publication_date: datetime
    photo: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

class NewsPaginationResponse(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool
    items: List[NewsResponse]

    class Config:
        arbitrary_types_allowed = True

class NewsPatch(BaseModel):
    params: Dict[str, Any]

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    @field_validator('params')
    def validate_individual_fields(v):
        for key in v:
            if key == 'title':
                NewsCreate.title_len(v[key])
            elif key == 'description':
                NewsCreate.description_len(v[key])
        return v