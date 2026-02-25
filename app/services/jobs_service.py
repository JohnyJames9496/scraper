from sqlalchemy.orm import Session
from app.database import models
from datetime import datetime, timedelta

def get_existing_links(db: Session):
    return {
        row[0] for row in db.query(models.Internship.link).all()
    }

def bulk_save_jobs(db: Session, jobs: list):
    if jobs:
        db.bulk_save_objects(jobs)
        db.commit()

def delete_old_jobs(db: Session, days: int = 14):
    cutoff = datetime.utcnow() - timedelta(days=days)
    db.query(models.Internship).filter(
        models.Internship.scraped_at < cutoff
    ).delete()
    db.commit()