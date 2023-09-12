from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..env import get_env

env = get_env()

SQLALCHEMY_DATABASE_URL = f"postgresql://{env.postgres_user}:{env.postgres_password}@{env.postgres_host}:{env.postgres_port}/{env.postgres_database}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()
