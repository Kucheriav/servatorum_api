from typing import List, Optional
from app.schemas.legal_entity_schema import (
    LegalEntityCreate, LegalEntityResponse, LegalEntityPatch,
    LegalEntityAccountDetailsCreate, LegalEntityAccountDetailsPatch
)


class FoundationCreate(LegalEntityCreate):
    account_details: List[LegalEntityAccountDetailsCreate]


class FoundationAccountDetailsResponse(LegalEntityAccountDetailsCreate):
    id: int


class FoundationResponse(LegalEntityResponse):
    account_details: List[FoundationAccountDetailsResponse]


class FoundationPatch(LegalEntityPatch):
    account_details: Optional[List[LegalEntityAccountDetailsPatch]] = None