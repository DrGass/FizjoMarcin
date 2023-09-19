from pydantic import BaseModel, ConfigDict


class NewPatient(BaseModel):
    name: str
    surname: str
    age: int
    owner_id: int

    model_config = ConfigDict()


class ShowPatient(BaseModel):
    name: str
    surname: str
    # owner : User didn't work for some unknown to me reason

    model_config = ConfigDict()
