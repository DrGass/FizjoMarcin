# from sqlalchemy import Column, Integer, String
# from app.modules.database import Base, SessionLocal
# from passlib.context import CryptContext
# from sqlalchemy.orm import relationship

# pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


# class User(Base):
#     __tablename__ = "user"

#     id = Column(Integer, primary_key=True)
#     username = Column(String)
#     password = Column(String)

#     patients = relationship("Patient", back_populates="users")


# @staticmethod
# def create_user(request):
#     new_user = User(**request.model_dump())
#     new_user.password = pwd_ctx.hash(request.password)
#     return new_user


# @staticmethod
# def get_user_by_id(id, session: SessionLocal):
#     data = session.query(User).filter(User.id == id).first()
#     return data


# @staticmethod
# def delete_user(id, session: SessionLocal):
#     session.query(User).filter(User.id == id).delete(synchronize_session=False)


# @staticmethod
# def update_user(id, session: SessionLocal, request):
#     session.query(User).filter(User.id == id).update(request.model_dump())

from fastapi import Depends, HTTPException, status
from sqlalchemy import Column, Integer, String
from app.modules.database import Base, SessionLocal, get_db
from passlib.context import CryptContext
from sqlalchemy.orm import relationship

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    patients = relationship("Patient", back_populates="users")


@staticmethod
def create_user(request, db: SessionLocal):
    new_user = User(**request.model_dump())
    new_user.password = pwd_ctx.hash(request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@staticmethod
def get_user_by_id(id, db: SessionLocal):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with number {id} is not avaiable",
        )
    return user


@staticmethod
def delete_user(id, db: SessionLocal):
    db.query(User).filter(User.id == id).delete(synchronize_session=False)
    db.commit()


@staticmethod
def update_user(id, db: SessionLocal, request):
    db.query(User).filter(User.id == id).update(request.model_dump())
    db.commit()

@staticmethod
def get_all_users(db: SessionLocal):
    return db.query(User).all()
