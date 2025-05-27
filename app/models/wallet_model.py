from sqlalchemy import Column, Integer, Float, Enum, UniqueConstraint
from app.database import Base


class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True)
    owner_type = Column(Enum('user', 'company', 'foundation', 'fundraising'), nullable=False)
    owner_id = Column(Integer, nullable=False)
    balance = Column(Float, default=0.0)

    __table_args__ = (
        UniqueConstraint('owner_type', 'owner_id', name='unique_owner_wallet'),
    )