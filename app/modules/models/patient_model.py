from sqlalchemy import Integer, String
from sqlalchemy.sql.schema import Column
from app.modules.database import Base, SessionLocal


class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    age = Column(Integer)


@staticmethod
def get_patient_by_id(id, session: SessionLocal):
    data = session.query(Patient).filter(Patient.id == id).first()
    return data


@staticmethod
def delete_patient(id, session: SessionLocal):
    session.query(Patient).filter(Patient.id == id).delete(synchronize_session=False)
