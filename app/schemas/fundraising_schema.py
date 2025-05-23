from pydantic import BaseModel, field_validator, ValidationError
from typing import Dict, Any, List
import datetime

class FundraisingCreate(BaseModel):
    title: str
    description: str
    goal_amount: float
    raised_amount: float
    start_date: datetime.date
    finish_date: datetime.date

    class Config:
        arbitrary_types_allowed = True

    @field_validator('start_date')
    @staticmethod
    def start_date_not_before_today(v):
        if v < datetime.datetime.now().date():
            raise ValidationError('Start date cannot be before today')
        return v

    @field_validator('finish_date')
    @staticmethod
    def finish_date_not_before_today(v):
        if v < datetime.datetime.now().date():
            raise ValidationError('Finish date cannot be before today')
        return v

class FundraisingResponce(BaseModel):
    fundraising_id: int
    title: str
    description: str
    goal_amount: float
    raised_amount: float
    start_date: datetime.date
    finish_date: datetime.date

    class Config:
        arbitrary_types_allowed = True

class FundraisingPaginationResponse(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool
    items: List[FundraisingResponce]

    class Config:
        arbitrary_types_allowed = True

class FundraisingPatch(BaseModel):
    params: Dict[str, Any]

    class Config:
        arbitrary_types_allowed = True

    @field_validator('params')
    @staticmethod
    def validate_individual_fields(v):
        for key in v:
            if key == 'start_date':
                FundraisingCreate.start_date_not_before_today(v[key])
            elif key == 'finish_date':
                FundraisingCreate.finish_date_not_before_today(v[key])
        return v