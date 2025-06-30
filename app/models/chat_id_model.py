from sqlalchemy import Column, Integer, String
from app.database import Base

class ChatIdList(Base):
    __tablename__ = "chat_id_list"
    id = Column(Integer, primary_key=True)
    chat_id = Column(String, nullable=False, unique=True)
