from fastapi import FastAPI

import sys
import os

sys.path.append(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/app")

from modules.database import engine
from routers import patient, user, authentication

import modules.models.patient_model as patient_model
import modules.models.user_model as user_model

app = FastAPI()

app.include_router(authentication.router)
app.include_router(patient.router)
app.include_router(user.router)

user_model.Base.metadata.create_all(bind=engine)
patient_model.Base.metadata.create_all(bind=engine)
