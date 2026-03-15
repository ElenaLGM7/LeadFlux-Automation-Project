from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, index=True)
    company = Column(String)
    message = Column(String)
    score = Column(Integer)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
