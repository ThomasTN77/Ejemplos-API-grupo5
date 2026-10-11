import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("Falta la variable DATABASE_URL. Revisa tu archivo .env")

opciones = {"pool_pre_ping": True}

if DATABASE_URL.startswith("sqlite"):
    opciones["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **opciones)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
