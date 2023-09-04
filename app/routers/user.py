from fastapi import APIRouter, Depends, status, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.modules.database import get_db

import app.modules.models.user_model as user_model
import app.modules.schemas.user_schema as user_schema
import app.modules.auth.oauth2 as oauth2

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/", response_model=list[user_schema.showUser])
def get_all(
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(oauth2.get_current_user),
):
    users = db.query(user_model.User).all()
    return users


@router.get("/{id}", status_code=200, response_model=user_schema.User)
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(oauth2.get_current_user),
):
    user = user_model.get_user_by_id(id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with number {id} is not avaiable",
        )
    return user


pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
    request: user_schema.User,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(oauth2.get_current_user),
):
    new_user = user_model.create_user(request)
    # new_user = user_model.User(**request.model_dump())
    # new_user.password = pwd_ctx.hash(new_user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"success": True, "created_id:": new_user.id}


@router.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(oauth2.get_current_user),
):
    user_model.delete_user(id, db)
    db.commit()
    return {"success": True, "deleted_id": id}


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(
    id,
    request: user_schema.User,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(oauth2.get_current_user),
):
    user_model.update_user(id, db, request)
    db.commit()
    return "updated"
