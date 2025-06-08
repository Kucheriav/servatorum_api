from pydantic import BaseModel
from typing import Optional

class SphereCreate(BaseModel):
    name: str

class SphereResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class SpherePatch(BaseModel):
    name: Optional[str] = None