from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.scraper.internshala_scraper import scrape_internshala

router = APIRouter(prefix="/internships", tags=["Internships"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/scrape")
async def run_scraper(keyword: str, db: Session = Depends(get_db)):
    count = await scrape_internshala(keyword, db)
    return {"scraped": count}