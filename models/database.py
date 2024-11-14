"""
This file is used to create a database connection and session for the application.
"""
# pylint: disable=missing-function-docstring
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.main import config

engine = create_engine(
    config.SQLALCHEMY_DATABASE_URL, pool_recycle=3600, pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class SessionManager:
    def __init__(self):
        self.session = SessionLocal()
        self.session.expire_on_commit = False

    def __enter__(self):
        return self.session

    def __exit__(self, type, value, traceback):
        self.session.close()


def get_db_session():
    return SessionManager()
