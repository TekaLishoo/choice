from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import Settings

actual_settings = Settings()

name_db = actual_settings.POSTGRES_NAME_DB
user_db = actual_settings.POSTGRES_USER
pass_db = actual_settings.POSTGRES_PASSWORD
host_db = actual_settings.POSTGRES_HOST

database_url = f"postgresql+psycopg2://{user_db}:{pass_db}@{host_db}/{name_db}"

engine = create_engine(database_url)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
