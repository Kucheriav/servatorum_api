from pydantic import BaseModel, Field
from typing import Optional, Dict

class RegistrationStepSchema(BaseModel):
    phone: str
    user_type: str  # "user", "fund", "company"
    step: int  # номер шага (1, 2 и т.д.)
    name: Optional[str]
    profile_picture: Optional[str]
    other_fields: Optional[Dict]  # остальные поля юзера
    fund_fields: Optional[Dict]   # поля фонда
    company_fields: Optional[Dict]