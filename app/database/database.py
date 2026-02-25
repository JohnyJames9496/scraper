import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

print("DATABASE_URL Loaded:", DATABASE_URL)

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set!")

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}  # Required for Supabase
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()