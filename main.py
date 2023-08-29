from fastapi import FastAPI, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db
import schemas, models

app = FastAPI()

models.Base.metadata.create_all(bind = engine)


@app.post('/patient',status_code=status.HTTP_201_CREATED)
def create(request: schemas.CreateNewPatient, db: Session = Depends(get_db)):
    to_create = models.Patient(
        id=request.id,
        name=request.name,
        surname=request.surname,
        age=request.age
    )
    db.add(to_create)
    db.commit()
    return{
        "success": True,
        "created_id": to_create.id
    }

@app.delete('/patient/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db:Session = Depends(get_db)):
    db.query(models.Patient).filter(models.Patient.id == id). delete(synchronize_session=False)
    db.commit()
    return{
        "success": True,
        "deleted_id": id
    }

@app.get("/patient")
def get_all(db : Session = Depends(get_db)):
    patients = db.query(models.Patient).all()
    return patients

@app.get("/patient/{id}", status_code=200)
def get_by_id(response : Response, id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Patient with number {id} is not avaiable')
    return patient

# @app.get("/")
# def get_by_id(id: int, db: Session = Depends(get_db)):
#     return db.query(Patient).filter(Patient.id == id).first()

# @app.delete('/')
# def delete(id: int, db: Session = Depends(get_db)):
#     db.query(Patient).filter(Patient.id == id).delete()
#     db.commit()
#     return {"success": True}

# @app.post('/user')
# def create_user(request: schemas.user)