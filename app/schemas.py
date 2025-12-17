from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Assessment Schemas
class AssessmentBase(BaseModel):
    test_name: str
    test_description: Optional[str] = None
    category: Optional[str] = None
    skills_assessed: Optional[str] = None
    duration_minutes: Optional[int] = None
    difficulty_level: Optional[str] = None

class AssessmentCreate(AssessmentBase):
    pass

class AssessmentResponse(AssessmentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Job Role Schemas
class JobRoleBase(BaseModel):
    role_name: str
    role_description: Optional[str] = None
    department: Optional[str] = None
    required_skills: Optional[str] = None

class JobRoleCreate(JobRoleBase):
    pass

class JobRoleResponse(JobRoleBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Recommendation Schemas
class RecommendationRequest(BaseModel):
    job_role: str = Field(..., min_length=2, max_length=255)
    top_k: Optional[int] = Field(5, ge=1, le=10)  # Return top 5 by default

class RecommendedTest(BaseModel):
    test_name: str
    test_description: Optional[str]
    category: Optional[str]
    confidence_score: float
    skills_match: Optional[str]

class RecommendationResponse(BaseModel):
    job_role: str
    recommendations: List[RecommendedTest]
    total_recommendations: int
    timestamp: datetime 
