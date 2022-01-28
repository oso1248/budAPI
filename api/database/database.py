# psycopg2 connection
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .. config import settings

# SQLALCHEMY orm connection
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from loguru import logger

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# psycopg2 connection
while True:
    try:
        conn = psycopg2.connect(host=settings.DATABASE_HOST, database=settings.DATABASE_NAME, user=settings.DATABASE_USERNAME,
                                password=settings.DATABASE_PASSWORD, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        break
    except Exception as error:
        logger.error(f'{error}')
        time.sleep(5)
