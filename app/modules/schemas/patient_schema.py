from pydantic import BaseModel


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
    # owner : User didn't work for some unknown to me reason

    class Config:
        from_attributes = True
