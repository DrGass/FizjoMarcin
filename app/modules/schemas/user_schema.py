from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    password: str


class showUser(BaseModel):
    email: str
    id: int
