from fastapi import FastAPI, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from app.modules.database import engine, get_db
from typing import List
import app.modules.schemas.patient_schema as patient_schema
import app.modules.models.patient_model as patient_model

app = FastAPI()

patient_model.Base.metadata.create_all(bind=engine)


@app.post("/patient", status_code=status.HTTP_201_CREATED)
def create(request: patient_schema.NewPatient, db: Session = Depends(get_db)):
    new_patient = patient_model.Patient(
        id=request.id, name=request.name, surname=request.surname, age=request.age
    )
    # I tried to replicate this one but didn't succeed, yet at least
    # new_patient = patient_model.Patient(new_patient : request)
    db.add(new_patient)
    db.commit()
    return {"success": True, "created_id": new_patient.id}


@app.delete("/patient/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    patient_model.delete_patient(id, db)
    db.commit()
    return {"success": True, "deleted_id": id}


@app.get("/patient", response_model=List[patient_schema.ShowPatient])
def get_all(db: Session = Depends(get_db)):
    patients = db.query(patient_model.Patient).all()
    return patients


@app.get("/patient/{id}", status_code=200, response_model=patient_schema.ShowPatient)
def get_by_id(id: int, db: Session = Depends(get_db)):
    patient = patient_model.get_patient_by_id(id, db)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with number {id} is not avaiable",
        )
    return patient
