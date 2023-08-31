from fastapi import APIRouter, Depends, Response, status, HTTPException

from sqlalchemy.orm import Session
from app.modules.database import engine, get_db

import app.modules.schemas.patient_schema as patient_schema
import app.modules.models.patient_model as patient_model

router = APIRouter()


@router.get(
    "/patient", response_model=list[patient_schema.ShowPatient], tags=["patient"]
)
def get_all(db: Session = Depends(get_db)):
    patients = db.query(patient_model.Patient).all()
    return patients


@router.get(
    "/patient/{id}",
    status_code=200,
    response_model=patient_schema.ShowPatient,
    tags=["patient"],
)
def get_by_id(id: int, db: Session = Depends(get_db)):
    patient = patient_model.get_patient_by_id(id, db)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with number {id} is not avaiable",
        )
    return patient
