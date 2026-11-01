import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

logger = logging.getLogger(__name__)

# Primary PostgreSQL URL, default password 'admin' as provided by user
PG_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:admin@localhost:5432/wearia_db")
SQLITE_URL = "sqlite:///./wearia.db"

Base = declarative_base()

def get_engine():
    # Attempt to connect to PostgreSQL; if unavailable, use SQLite fallback
    try:
        engine = create_engine(PG_URL, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info(f"Connected to PostgreSQL database at {PG_URL}")
        return engine
    except Exception as e:
        logger.warning(f"PostgreSQL connection failed ({e}). Falling back to local SQLite database.")
        engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
        return engine

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
