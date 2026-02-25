from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.database import models


def cleanup_old_internships(db: Session, days: int = 7):
    cutoff = date.today() - timedelta(days=days)

    deleted = db.query(models.Internship)\
        .filter(models.Internship.scraped_date < cutoff)\
        .delete()

    db.commit()
    return deleted