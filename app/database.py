from sqlalchemy import create_engine #needed to create connection instance to DB
from sqlalchemy.ext.declarative import declarative_base #needed to create / return base object needed for DB tables class definition in python
from sqlalchemy.orm import sessionmaker #needed to return session class -> for managing DB operations

SQLALCHEMY_DATABASE_URL = "postgresql://sylwestersojka:123@localhost/fastapi_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()

def get_sql_db():
    conn = SessionLocal()
    try:
        yield conn
    finally:
        if conn:
            conn.close()