from fastapi import FastAPI
from app.core.browser import start_browser, stop_browser
from app.api.scrape_routes import router as scrape_router

app = FastAPI(title="Internship Scraper API")

@app.on_event("startup")
async def startup():
    await start_browser()

@app.on_event("shutdown")
async def shutdown():
    await stop_browser()

app.include_router(scrape_router)