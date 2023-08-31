from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from app.modules.database import Base, SessionLocal
from passlib.context import CryptContext
from sqlalchemy.orm import relationship

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)

    patients = relationship("Patient", back_populates="users")


@staticmethod
def create_user(request):
    new_user = User(**request.model_dump())
    new_user.password = pwd_ctx.hash(new_user.password)
    return new_user


@staticmethod
def get_user_by_id(id, session: SessionLocal):
    data = session.query(User).filter(User.id == id).first()
    return data


@staticmethod
def delete_user(id, session: SessionLocal):
    session.query(User).filter(User.id == id).delete(synchronize_session=False)


@staticmethod
def update_user(id, session: SessionLocal, request):
    session.query(User).filter(User.id == id).update(request.model_dump())
