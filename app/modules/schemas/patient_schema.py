from pydantic import BaseModel
from app.modules.schemas.user_schema import showUser
from app.modules.database import SessionLocal


class NewPatient(BaseModel):
    id: int
    name: str
    surname: str
    age: int
# can't figure out how to connect it dynamically 
    user : showUser


class ShowPatient(BaseModel):
    name: str
    surname: str
