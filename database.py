from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator
from sqlalchemy.future import Engine

DATABASE_URL = "postgresql://postgres:yyk15793@localhost:5432/QuizApplication"

# SQLAlchemy motoru oluştur
engine = create_engine(DATABASE_URL)

# Oturum üreticisi oluştur
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Temel model sınıfı
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
