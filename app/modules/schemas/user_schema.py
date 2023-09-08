from pydantic import BaseModel

from modules.schemas.patient_schema import ShowPatient


class User(BaseModel):
    id: int
    username: str
    password: str

    class Config:
        from_attributes = True


class showUser(BaseModel):
    username: str
    id: int
    patients: list[ShowPatient] = []

    class Config:
        from_attributes = True
