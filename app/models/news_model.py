from sqlalchemy import Column, Integer, String, Date, Float
from app.database import Base

class News(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    publication_date = Column(Date, nullable=False)
    photo = Column(String)