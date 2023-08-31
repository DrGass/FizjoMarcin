from pydantic import BaseModel
from app.modules.schemas.patient_schema import ShowPatient


class User(BaseModel):
    id: int
    email: str
    password: str

    class Config:
        from_attributes = True


class showUser(BaseModel):
    email: str
    id: int
    patients: list[ShowPatient] = []

    class Config:
        from_attributes = True
