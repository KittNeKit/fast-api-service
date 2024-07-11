from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.config import settings

SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    from api.models import Base
    Base.metadata.create_all(bind=engine)
