from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Enum
from app.database import Base


class Fundraising(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    goal_amount = Column(Float)
    raised_amount = Column(Float)
    start_date = Column(Date)
    finish_date = Column(Date)
    owner_id = Column(Integer, ForeignKey('users.id'))
    fund_id = Column(Integer, ForeignKey('funds.id'))


class FundraisingFiles(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    path = Column(String)
    file_type = Column(Enum("doc", "photo", name="file_type_enum"))
