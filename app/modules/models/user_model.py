from fastapi import HTTPException, status
from sqlalchemy import Column, Integer, String

from modules.database import Base, SessionLocal
from passlib.context import CryptContext
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
from ..exceptions import UserExistsException

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    password = Column(String)

    patients = relationship("Patient", back_populates="users")


@staticmethod
def create_user(request, db: SessionLocal):
    new_user = User(**request.model_dump())
    new_user.password = pwd_ctx.hash(request.password)
    try:
        db.add(new_user)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise UserExistsException
    db.refresh(new_user)
    return new_user


@staticmethod
def get_user_by_id(id, db: SessionLocal):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with number {id} is not avaiable",
        )
    return user


@staticmethod
def delete_user(id, db: SessionLocal):
    db.query(User).filter(User.id == id).delete(synchronize_session=False)
    db.commit()


@staticmethod
def update_user(id, db: SessionLocal, request):
    user = db.query(User).filter(User.id == id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )

    user.update(request.dict())
    db.commit()


@staticmethod
def get_all_users(db: SessionLocal):
    return db.query(User).all()


################################### ! Code before model update
# from sqlalchemy import Column, Integer, String
# from modules.database import Base, SessionLocal
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
# def get_user_by_id(id, db: SessionLocal):
#     data = db.query(User).filter(User.id == id).first()
#     return data


# @staticmethod
# def delete_user(id, db: SessionLocal):
#     db.query(User).filter(User.id == id).delete(synchronize_session=False)


# @staticmethod
# def update_user(id, db: SessionLocal, request):
#     db.query(User).filter(User.id == id).update(request.model_dump())
