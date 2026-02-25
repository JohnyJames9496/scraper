from sqlalchemy.orm import Session
from app.database import models

def get_existing_links(db: Session):
    return {
        row[0] for row in db.query(models.Internship.link).all()
    }

def bulk_save_jobs(db: Session, jobs: list):
    if jobs:
        db.bulk_save_objects(jobs)
        db.commit()