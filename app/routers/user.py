from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from modules.database import get_db

import modules.models.user_model as user_model
import modules.schemas.user_schema as user_schema
import modules.auth.oauth2 as oauth2

router = APIRouter(prefix="/user", tags=["User"])


@router.get(
    "/",
    response_model=list[user_schema.showUser],
    dependencies=[Depends(oauth2.get_current_user)],
)
def get_all(
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(oauth2.get_current_user),
):
    users = user_model.get_all_users(db)
    return users


@router.get("/{id}", status_code=200, response_model=user_schema.showUser)
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(oauth2.get_current_user),
):
    user = user_model.get_user_by_id(id, db)
    return user


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create(
    request: user_schema.User,
    db: Session = Depends(get_db),
):
    new_user = user_model.create_user(request, db)
    return {"success": True, "created_id:": new_user.id}


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(oauth2.get_current_user),
):
    user_model.delete_user(id, db)
    return {"success:": True}


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(
    id,
    request: user_schema.User,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(oauth2.get_current_user),
):
    user_model.update_user(id, db, request)
    return {"success:": True, "Updated user nr:": id}
