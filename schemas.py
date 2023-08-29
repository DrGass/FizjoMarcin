from pydantic import BaseModel

class CreateNewPatient(BaseModel):
    id : int
    name : str
    surname : str
    age : int

class User(BaseModel):
    name:str
    email:str
    password:str