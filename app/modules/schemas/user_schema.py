from pydantic import BaseModel,ConfigDict

from modules.schemas.patient_schema import ShowPatient


class User(BaseModel):
    id: int
    username: str
    password: str

    model_config = ConfigDict()


class showUser(BaseModel):
    username: str
    id: int
    patients: list[ShowPatient] = []

    model_config = ConfigDict()
