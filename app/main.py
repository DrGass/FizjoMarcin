from fastapi import FastAPI, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from app.modules.database import engine, get_db
from typing import List
import app.modules.schemas as schemas
import app.modules.models as models

app = FastAPI()

models.Base.metadata.create_all(bind = engine)


@app.post('/patient',status_code=status.HTTP_201_CREATED)
def create(request: schemas.CreateNewPatient, db: Session = Depends(get_db)):
    new_patient = models.Patient(
        id=request.id,
        name=request.name,
        surname=request.surname,
        age=request.age
)   
    db.add(new_patient)
    db.commit()
    return{
        "success": True,
        "created_id": new_patient.id
    }

@app.delete('/patient/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db:Session = Depends(get_db)):
    db.query(models.Patient).filter(models.Patient.id == id). delete(synchronize_session=False)
    db.commit()
    return{
        "success": True,
        "deleted_id": id
    }

@app.get("/patient",response_model=List[schemas.ShowPatient])
def get_all(db : Session = Depends(get_db)):
    patients = db.query(models.Patient).all()
    return patients

@app.get("/patient/{id}", status_code=200, response_model=schemas.ShowPatient)
def get_by_id(response : Response, id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Patient with number {id} is not avaiable')
    return patient