from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Assessment(Base):
    """Table to store SHL assessment tests"""
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    test_name = Column(String(255), nullable=False, unique=True)
    test_description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)  # Technical, Behavioral, Cognitive
    skills_assessed = Column(Text, nullable=True)  # Comma-separated skills
    duration_minutes = Column(Integer, nullable=True)
    difficulty_level = Column(String(50), nullable=True)  # Easy, Medium, Hard
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Assessment {self.test_name}>"


class JobRole(Base):
    """Table to store job roles"""
    __tablename__ = "job_roles"
    
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(255), nullable=False, unique=True)
    role_description = Column(Text, nullable=True)
    department = Column(String(100), nullable=True)
    required_skills = Column(Text, nullable=True)  # Comma-separated skills
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<JobRole {self.role_name}>"


class Recommendation(Base):
    """Table to store recommendation history"""
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    job_role = Column(String(255), nullable=False)
    recommended_tests = Column(Text, nullable=False)  # JSON string
    confidence_score = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Recommendation for {self.job_role}>" 
