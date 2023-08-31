from fastapi import FastAPI, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from app.modules.database import engine, get_db
from typing import List
from passlib.context import CryptContext

import app.modules.schemas.patient_schema as patient_schema
import app.modules.models.patient_model  as patient_model
import app.modules.models.user_model as user_model
import app.modules.schemas.user_schema as user_schema

app = FastAPI()

patient_model.Base.metadata.create_all(bind=engine)
user_model.Base.metadata.create_all(bind=engine)


@app.post("/patient", status_code=status.HTTP_201_CREATED)
def create(request: patient_schema.NewPatient, db: Session = Depends(get_db)):
    new_patient = patient_model.Patient(request.model_dump())
    db.add(new_patient)
    db.commit()
    return {"success": True, "created_id": new_patient.id}


@app.delete("/patient/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    patient_model.delete_patient(id, db)
    db.commit()
    return {"success": True, "deleted_id": id}

@app.put('/patient/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id,request: patient_schema.NewPatient,db: Session = Depends(get_db)):
    patient_model.update_patient(id,db,request)
    db.commit()
    return 'updated'


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

# User 

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated = "auto")

@app.post("/user", status_code=status.HTTP_201_CREATED)
def create(request: user_schema.User, db: Session = Depends(get_db)):
    # new_user = user_model.create_user(request)
    new_user = user_model.User(**request.model_dump())
    new_user.password = pwd_ctx.hash(new_user.password)
    db.add(new_user)
    db.commit()
    return {'success': True, "created_id:": new_user.id}

@app.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    user_model.delete_user(id, db)
    db.commit()
    return {"success": True, "deleted_id": id}

@app.put('/user/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id,request: user_schema.User,db: Session = Depends(get_db)):
    user_model.update_user(id,db,request)
    db.commit()
    return 'updated'

@app.get("/user", response_model=List[user_schema.User])
def get_all(db: Session = Depends(get_db)):
    patients = db.query(user_model.User).all()
    return patients

@app.get("/user/{id}", status_code=200, response_model=user_schema.User)
def get_by_id(id: int, db: Session = Depends(get_db)):
    patient = user_model.get_user_by_id(id, db)
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with number {id} is not avaiable",
        )
    return patient