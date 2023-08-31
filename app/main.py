from fastapi import FastAPI
from app.modules.database import engine
from app.routers import patient, user

import app.modules.models.patient_model as patient_model
import app.modules.models.user_model as user_model

app = FastAPI()
app.include_router(patient.router)
app.include_router(user.router)

user_model.Base.metadata.create_all(bind=engine)
patient_model.Base.metadata.create_all(bind=engine)
