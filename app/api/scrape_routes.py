from fastapi import APIRouter
from app.database.database import SessionLocal
from app.scrapers.internshala import scrape_internshala

router = APIRouter(prefix="/scrape", tags=["Scraper"])

@router.get("/{keyword}")
async def scrape(keyword: str):
    db = SessionLocal()
    try:
        print("Scrape endpoint called with:", keyword)
        count = await scrape_internshala(keyword, db)
        print("Scrape finished. Saved:", count)
        return {"saved": count}
    except Exception as e:
        print("ERROR OCCURRED IN ENDPOINT:", str(e))
        raise e
    finally:
        db.close()