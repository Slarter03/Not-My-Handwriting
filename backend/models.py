from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class StudentProfile(Base):
    __tablename__ = 'student_profiles'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    submissions = relationship("Submission", back_populates="student")

class Submission(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student_profiles.id'), nullable=False)
    submission_date = Column(String, nullable=False)
    content = Column(String, nullable=False)

    student = relationship("StudentProfile", back_populates="submissions")
