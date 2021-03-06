import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dependencies import get_db_settings

settings = get_db_settings()

SQLALCHEMY_DATABASE_URL = \
    f"postgresql+psycopg2://{settings.username}:{settings.password}@db:{settings.port}/{settings.database}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

database = databases.Database(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()
