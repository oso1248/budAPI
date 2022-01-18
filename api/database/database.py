# psycopg2 connection
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# SQLALCHEMY orm connection
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://adamcoulson:adamcoulson@localhost/budAPI"
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
        conn = psycopg2.connect(host='localhost', database='budAPI', user='adamcoulson',
                                password='adamcoulson', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        break
    except Exception as error:
        print('conn fail')
        print('Error', error)
        time.sleep(5)
