from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UserWalletTransactionBase(BaseModel):
    type: str = Field(..., description="Тип операции: deposit или withdrawal")
    amount: float = Field(..., gt=0, description="Сумма операции")
    comment: Optional[str] = Field(None, description="Комментарий к операции")

class UserWalletTransactionCreate(UserWalletTransactionBase):
    pass

class UserWalletTransactionResponse(UserWalletTransactionBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class WalletBalanceResponse(BaseModel):
    user_id: int
    balance: float

class WalletHistoryResponse(BaseModel):
    user_id: int
    history: List[UserWalletTransactionResponse]