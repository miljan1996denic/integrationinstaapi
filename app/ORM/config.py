from contextlib import contextmanager
from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

SQLALCHEMY_DATABASE_URL = (
        f"postgresql://"
     f"{getenv('PGUSER')}:"
     f"{getenv('PGPASSWORD')}@"
     f"{getenv('DATABASE_URI')}:"
     f"{getenv('DATABASE_PORT','5432')}/"
    f"{getenv('DATABASE_NAME')}"
  )


engine = create_engine (SQLALCHEMY_DATABASE_URL, connect_args={}, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_manager = contextmanager(get_db)
