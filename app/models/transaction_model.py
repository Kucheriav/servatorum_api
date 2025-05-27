from sqlalchemy import Column, Integer, Float, String, Enum, ForeignKey, DateTime
from app.database import Base
import datetime

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    # null если операция с внешней системой
    sender_wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=True)
    recipient_wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=True)
    # тип операции: deposit, withdrawal, transfer
    type = Column(Enum('deposit', 'withdrawal', 'transfer'), nullable=False)
    amount = Column(Float, nullable=False)
    comment = Column(String)
