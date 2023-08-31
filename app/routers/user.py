from fastapi import APIRouter, Depends, Response, status, HTTPException

from sqlalchemy.orm import Session
from app.modules.database import engine, get_db

import app.modules.models.user_model as user_model
import app.modules.schemas.user_schema as user_schema

router = APIRouter()

@router.get("/user", response_model=list[user_schema.showUser], tags=["user"])
def get_all(db: Session = Depends(get_db)):
    patients = db.query(user_model.User).all()
    return patients


@router.get(
    "/user/{id}", status_code=200, response_model=user_schema.showUser, tags=["user"]
)
def get_by_id(id: int, db: Session = Depends(get_db)):
    patient = user_model.get_user_by_id(id, db)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with number {id} is not avaiable",
        )
    return patient
