from sqlalchemy import Column, Integer, String, Text
from .database import Base


class ResumeAnalysis(Base):

    __tablename__ = "resume_analysis"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    filename = Column(
        String(255)
    )

    resume_skills = Column(
        Text
    )

    job_skills = Column(
        Text
    )

    matched_skills = Column(
        Text
    )

    missing_skills = Column(
        Text
    )

    match_percentage = Column(
        String(20)
    )

    ai_analysis = Column(
        Text
    )