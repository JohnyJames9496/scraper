from sqlalchemy import Column, Integer, String, Date
from datetime import date
from app.database.database import Base


class Internship(Base):
    __tablename__ = "internships_new"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)
    company = Column(String(100), nullable=False)
    link = Column(String, unique=True, nullable=False)

    source = Column(String(50))
    keyword = Column(String(100))

    location = Column(String(100))
    duration = Column(String(50))
    stipend = Column(String(100))
    skills = Column(String(200))

    scraped_date = Column(Date, nullable=False, default=date.today)