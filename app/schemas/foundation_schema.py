from typing import List, Optional
from app.schemas.legal_entity_schema import (
    LegalEntityCreate, LegalEntityResponse, LegalEntityPatch,
    LegalEntityAccountDetailsCreate, LegalEntityAccountDetailsPatch
)


class FoundationCreate(LegalEntityCreate):
    account_details: LegalEntityAccountDetailsCreate

class FoundationAccountDetailsResponse(LegalEntityAccountDetailsCreate):
    id: int

class FoundationResponse(LegalEntityResponse):
    account_details: List[FoundationAccountDetailsResponse]

class FoundationPatch(LegalEntityPatch):
    # PATCH — обновление фонда и реквизитов по id
    account_details: Optional[List[LegalEntityAccountDetailsPatch]] = None

# Для POST (добавление нового счета)
class FoundationAccountDetailsAdd(LegalEntityAccountDetailsCreate):
    pass

class FoundationAccountDetailsAddResponse(FoundationAccountDetailsResponse):
    id: int