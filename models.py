from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class Feedback(Base):
    __tablename__ = "Feedback"
    __table_args__ = {"schema": "Volha_Platnitskaya_feedback"}

    feedbackId = Column(Integer, primary_key=True, autoincrement=True)
    submissionId = Column(Integer)
    score = Column(Integer)
    comment = Column(String)
    createdAt = Column(DateTime)