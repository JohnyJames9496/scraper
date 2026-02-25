from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from app.database.database import Base

class Internshipss(Base):
    __tablename__ = "internshipss"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    company = Column(String(100))
    link = Column(String(500), unique=True, index=True)
    source = Column(String(50))
    keyword = Column(String(100))
    location = Column(String(100))
    duration = Column(String(50))
    stipend = Column(String(100))
    skills = Column(String(200))
    scraped_at = Column(DateTime, default=datetime.utcnow, index=True)