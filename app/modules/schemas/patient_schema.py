from pydantic import BaseModel

from app.modules.database import SessionLocal


class NewPatient(BaseModel):
    id: int
    name: str
    surname: str
    age: int


class ShowPatient(BaseModel):
    name: str
    surname: str
