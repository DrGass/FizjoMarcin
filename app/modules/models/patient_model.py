from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm import relationship
from app.modules.database import Base, SessionLocal
from app.modules.schemas.user_schema import showUser


class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    age = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id"), nullable= True)

    users = relationship("User", back_populates="patients")


@staticmethod
def get_patient_by_id(id, session: SessionLocal):
    data = session.query(Patient).filter(Patient.id == id).first()
    return data


@staticmethod
def delete_patient(id, session: SessionLocal):
    session.query(Patient).filter(Patient.id == id).delete(synchronize_session=False)


@staticmethod
def update_patient(id, session: SessionLocal, request):
    session.query(Patient).filter(Patient.id == id).update(request.model_dump())
