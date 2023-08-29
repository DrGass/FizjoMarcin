from fastapi import FastAPI

app = FastAPI()

class Patient(BaseModel):
    id : int
    name : str
    surname : str
    age : int


@app.post("/patient")
def patient(request: Patient):
    return {f"Patient {request.name} {request.surname}, age: {request.age} has next visit on: {request.next_visit}"}

