from pydantic import BaseModel

class CreateNewPatient(BaseModel):
    id : int
    name : str
    surname : str
    age : int

class ShowPatient(BaseModel):
    name : str
    surname : str


class User(BaseModel):
    name:str
    email:str
    password:str
    phone_number:int