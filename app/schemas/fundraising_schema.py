from pydantic import BaseModel, field_validator
from typing import Dict, Any, List
from datetime import datetime

class FundraisingCreate(BaseModel):
    title: str
    description: str
    goal_amount: float
    raised_amount: float
    start_date: datetime.date
    finish_date: datetime.date

    @field_validator('start_date')
    def start_date_not_before_today(self, v):
        if v < datetime.now().date():
            raise ValueError('Start date cannot be before today')
        return v

    @field_validator('finish_date')
    def finish_date_not_before_today(self, v):
        if v < datetime.now().date():
            raise ValueError('Finish date cannot be before today')
        return v

class FundraisingResponce(BaseModel):
    title: str
    description: str
    goal_amount: float
    raised_amount: float
    start_date: datetime.date
    finish_date: datetime.date

class FundraisingPaginationResponse(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool
    fundraisings: List[FundraisingResponce]

class FundraisingPatch(BaseModel):
    fundraising_id: int
    params: Dict[str, Any]

    @field_validator('params')
    def validate_individual_fields(self, v):
        for key in v:
            if key == 'start_date':
                self.start_date_not_before_today(v[key])
            elif key == 'finish_date':
                self.finish_date_not_before_today(v[key])
        return v