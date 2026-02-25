from fastapi import FastAPI
from app.database.database import engine
from app.database import models
from app.routes import internship_routes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(internship_routes.router)