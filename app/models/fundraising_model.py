from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Enum, CheckConstraint
from app.database import Base


class Fundraising(Base):
    __tablename__ = "fundraisings"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    goal_amount = Column(Float)
    raised_amount = Column(Float)
    start_date = Column(Date)
    finish_date = Column(Date)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    __table_args__ = (
        CheckConstraint('start_date >= CURRENT_DATE'),
        CheckConstraint('finish_date >= CURRENT_DATE'),
        CheckConstraint('finish_date > start_date'),
    )

class FundraisingFiles(Base):
    __tablename__ = "fundraising_files"
    id = Column(Integer, primary_key=True, index=True)
    fundraise_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    name = Column(String)
    path = Column(String)
    file_type = Column(Enum("doc", "photo", name="file_type_enum"))
