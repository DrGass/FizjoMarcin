from pydantic import BaseModel, ValidationError
from app.modules.database import SessionLocal


class NewPatient(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    owner_id: int

    class Config:
        from_attributes = True


class ShowPatient(BaseModel):
    name: str
    surname: str
    # owner : User

    class Config:
        from_attributes = True
