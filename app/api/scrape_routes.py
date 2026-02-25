from fastapi import APIRouter
from app.database.database import SessionLocal
from app.scrapers.internshala import scrape_internshala

router = APIRouter(prefix="/scrape", tags=["Scraper"])

@router.get("/{keyword}")
async def scrape(keyword: str):
    db = SessionLocal()
    try:
        count = await scrape_internshala(keyword, db)
        return {"saved": count}
    finally:
        db.close()