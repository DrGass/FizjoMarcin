from fastapi import HTTPException, status
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm import relationship

from modules.database import Base, SessionLocal


class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    age = Column(Integer)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=True)

    users = relationship("User", back_populates="patients")


@staticmethod
def create_patient(request, session: SessionLocal):
    new_patient = Patient(**request.model_dump())
    session.add(new_patient)
    session.commit()
    session.refresh(new_patient)
    return new_patient


@staticmethod
def get_patient_by_id(id, session: SessionLocal):
    patient = session.query(Patient).filter(Patient.id == id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with number {id} is not avaiable",
        )
    return patient


@staticmethod
def delete_patient(id, session: SessionLocal):
    session.query(Patient).filter(Patient.id == id).delete(synchronize_session=False)
    session.commit()


@staticmethod
def update_patient(id, session: SessionLocal, request):
    patient = session.query(Patient).filter(Patient.id == id)
    if not patient.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with id {id} not found",
        )
    patient.update(request.dict())
    session.commit()
