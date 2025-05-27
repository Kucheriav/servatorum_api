from sqlalchemy import Column, Integer, Float,  String, ForeignKey
from app.database import Base


class UserWalletTransaction(Base):
    __tablename__ = "user_wallet_transactions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    type = Column(String, nullable=False)  # 'deposit' или 'withdrawal'
    amount = Column(Float, nullable=False)
    comment = Column(String)  # например, "Пополнение", "Пожертвование в фонд N", и т.п.