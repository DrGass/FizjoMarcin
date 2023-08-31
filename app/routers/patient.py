from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session
from app.modules.database import get_db

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

@router.post("/patient", status_code=status.HTTP_201_CREATED, tags=["patient"])
def create(request: patient_schema.NewPatient, db: Session = Depends(get_db)):
    new_patient = patient_model.Patient(**request.model_dump())
    new_patient.owner_id = (request.id,)
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return {"success": True, "created_id": new_patient.id}


@router.delete("/patient/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["patient"])
def destroy(id: int, db: Session = Depends(get_db)):
    patient_model.delete_patient(id, db)
    db.commit()
    return {"success": True, "deleted_id": id}


@router.put("/patient/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["patient"])
def update(id, request: patient_schema.NewPatient, db: Session = Depends(get_db)):
    patient_model.update_patient(id, db, request)
    db.commit()
    return "updated"
