from fastapi import FastAPI, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from app.modules.database import engine, get_db
from typing import List
from app.routers import patient, user

import app.modules.schemas.patient_schema as patient_schema
import app.modules.models.patient_model as patient_model
import app.modules.models.user_model as user_model
import app.modules.schemas.user_schema as user_schema

app = FastAPI()
app.include_router(patient.router)
app.include_router(user.router)


user_model.Base.metadata.create_all(bind=engine)
patient_model.Base.metadata.create_all(bind=engine)