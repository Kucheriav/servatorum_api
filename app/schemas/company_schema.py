from typing import Optional
from app.schemas.legal_entity_schema import (LegalEntityCreate, LegalEntityResponse, LegalEntityPatch,
                                             LegalEntityAccountDetailsCreate, LegalEntityAccountDetailsPatch)


class CompanyCreate(LegalEntityCreate):
    account_details: LegalEntityAccountDetailsCreate

class CompanyAccountDetailsResponse(LegalEntityAccountDetailsCreate):
    id: int

class CompanyResponse(LegalEntityResponse):
    account_details: CompanyAccountDetailsResponse

class CompanyPatch(LegalEntityPatch):
    account_details: Optional[LegalEntityAccountDetailsPatch] = None