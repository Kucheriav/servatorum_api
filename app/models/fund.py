from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..database import Base



fund_charity_sphere_association = Table(
    'fund_charity_sphere',
    Base.metadata,
    Column('fund_id', Integer, ForeignKey('funds.id'), primary_key=True),
    Column('charity_sphere_id', Integer, ForeignKey('charity_sphere.id'), primary_key=True)
)


class CharitySphere(Base):
    __tablename__ = 'charity_sphere'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # funds = relationship("Fund", secondary=fund_charity_sphere_association, back_populates="charity_spheres")



class Fund(Base):
    __tablename__ = "funds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    admin_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    inn = Column(String, nullable=False)
    kpp = Column(String, nullable=False)
    address = Column(String, nullable=False)
    profile_picture = Column(String)
    phone = Column(String, nullable=False)
    email = Column(String)
    website = Column(String)

    # fundraisings = relationship("Fundraising", back_populates="fund")
    # posts = relationship("Post", back_populates="fund")
    # accounts = relationship("Account", back_populates="fund")
    # charity_spheres = relationship("CharitySphere", secondary=fund_charity_sphere_association, back_populates="funds")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey('funds.id'), nullable=False)
    name = Column(String, nullable=False)
    bic = Column(String, nullable=False)
    ks_number = Column(String, nullable=False)
    account_number = Column(String, nullable=False)

    # fund = relationship("Fund", back_populates="accounts")