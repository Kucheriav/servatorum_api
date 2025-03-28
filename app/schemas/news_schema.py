from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class NewsCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: str = Field(..., max_length=1000)
    publication_date: datetime
    photo: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

class NewsResponse(BaseModel):
    id: int
    title: str
    description: str
    publication_date: datetime
    photo: Optional[str] = None


    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class NewsPaginationResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool
    items: List[NewsResponse]

class NewsUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    publication_date: Optional[datetime] = None
    photo: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True