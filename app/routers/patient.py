from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session
from app.modules.database import get_db

import app.modules.schemas.patient_schema as patient_schema
import app.modules.models.patient_model as patient_model
import app.modules.schemas.user_schema as user_schema
import app.routers.authentication as auth

router = APIRouter(prefix="/patient", tags=["Patient"])


@router.get("/", response_model=list[patient_schema.ShowPatient])
def get_all(
    db: Session = Depends(get_db),
    get_current_user: user_schema.User = Depends(auth.get_current_user),
):
    patients = db.query(patient_model.Patient).all()
    return patients


@router.get(
    "/{id}",
    status_code=200,
    response_model=patient_schema.ShowPatient,
)
def get_by_id(
    id: int,
    db: Session = Depends(get_db),
    get_current_user: user_schema.User = Depends(auth.get_current_user),
):
    patient = patient_model.get_patient_by_id(id, db)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with number {id} is not avaiable",
        )
    return patient


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
    request: patient_schema.NewPatient,
    db: Session = Depends(get_db),
    get_current_user: user_schema.User = Depends(auth.get_current_user),
):
    new_patient = patient_model.Patient(**request.model_dump())
    new_patient.owner_id = (request.id,)
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return {"success": True, "created_id": new_patient.id}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(
    id: int,
    db: Session = Depends(get_db),
    get_current_user: user_schema.User = Depends(auth.get_current_user),
):
    patient_model.delete_patient(id, db)
    db.commit()
    return {"success": True, "deleted_id": id}


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(
    id,
    request: patient_schema.NewPatient,
    db: Session = Depends(get_db),
    get_current_user: user_schema.User = Depends(auth.get_current_user),
):
    patient_model.update_patient(id, db, request)
    db.commit()
    return "updated"
