from pydantic import BaseModel
from datetime import datetime

class InternshipOut(BaseModel):
    title: str
    company: str
    link: str
    source: str
    location: str
    duration: str
    stipend: str
    skills: str
    scraped_at: datetime

    class Config:
        from_attributes = True