from pydantic import BaseModel, Field, field_validator, ValidationError, model_validator
from typing import Optional, List, Literal, Dict, Any
from datetime import datetime

class TransactionCreate(BaseModel):
    sender_wallet_id: Optional[int] = Field(None, description="ID кошелька-отправителя (None для пополнения)")
    recipient_wallet_id: Optional[int] = Field(None, description="ID кошелька-получателя (None для снятия)")
    type: Literal['deposit', 'withdrawal', 'transfer'] = Field(..., description="Тип операции: пополнение, снятие, перевод")
    amount: float = Field(..., gt=0, description="Сумма операции (>0)")
    comment: Optional[str] = Field(None, max_length=300, description="Комментарий к операции (макс. 300 символов)")

    @field_validator('type')
    @staticmethod
    def type_valid(v):
        if v not in ['deposit', 'withdrawal', 'transfer']:
            raise ValueError("Недопустимый тип транзакции")
        return v

    @field_validator('sender_wallet_id', 'recipient_wallet_id')
    @staticmethod
    def wallet_id_positive(v):
        if v is not None and v <= 0:
            raise ValueError("ID кошелька должен быть положительным")
        return v

    @field_validator('comment')
    @staticmethod
    def comment_length(v):
        if v is not None and len(v) > 300:
            raise ValueError("Комментарий не должен превышать 300 символов")
        return v

    @model_validator(mode="after")
    def check_sender_or_recipient(self):
        if self.sender_wallet_id is None and self.recipient_wallet_id is None:
            raise ValueError(
                "Хотя бы одно из полей sender_wallet_id или recipient_wallet_id должно быть заполнено")
        return self

class TransactionResponse(BaseModel):
    transaction_id: int
    type: str
    amount: float
    sender_wallet_id: Optional[int]
    recipient_wallet_id: Optional[int]
    comment: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

class TransactionPatch(BaseModel):
    params: Dict[str, Any]

    @field_validator('params')
    @staticmethod
    def validate_individual_fields(v):
        for key in v:
            if key == 'amount':
                if v[key] <= 0:
                    raise ValueError("Сумма должна быть положительной")
            if key == 'type':
                TransactionCreate.type_valid(v[key])
            if key == 'comment':
                TransactionCreate.comment_length(v[key])
        return v

    @model_validator(mode="after")
    def check_sender_or_recipient(self):
        if self.sender_wallet_id is None and self.recipient_wallet_id is None:
            raise ValueError(
                "Хотя бы одно из полей sender_wallet_id или recipient_wallet_id должно быть заполнено")
        return self