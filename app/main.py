from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from datetime import datetime
import json
# Updated: Add seed endpoint
from fastapi import FastAPI, Depends, HTTPException
# Import from our app modules
from app.database import engine, get_db, Base, SessionLocal
from app import models, schemas
from app.ml_model import recommendation_engine

# Create all tables in database
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app - ONLY ONCE!
app = FastAPI(
    title="SHL Assessment Recommendation Engine",
    description="AI-powered test recommendation system for talent assessment",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# THIS LINE WAS MISSING - Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add startup event to train model
@app.on_event("startup")
async def startup_event():
    """Train ML model when application starts"""
    print("\n" + "="*50)
    print("🚀 Initializing SHL Recommendation Engine...")
    print("="*50)
    
    db = SessionLocal()
    try:
        recommendation_engine.train(db)
        print("✅ ML Model ready!\n")
    except Exception as e:
        print(f"❌ Error training model: {e}\n")
    finally:
        db.close()

@app.get("/")
async def root():
    return {
        "message": "SHL Recommendation Engine API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "ui": "/static/index.html"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

@app.get("/db-status")
async def database_status(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))   
        return {
            "status": "connected",
            "database": "PostgreSQL",
            "message": "Database connection successful"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/assessments", response_model=List[schemas.AssessmentResponse])
async def get_all_assessments(db: Session = Depends(get_db)):
    """Get all available assessments"""
    assessments = db.query(models.Assessment).all()
    return assessments

@app.get("/assessments/{assessment_id}", response_model=schemas.AssessmentResponse)
async def get_assessment(assessment_id: int, db: Session = Depends(get_db)):
    """Get specific assessment by ID"""
    assessment = db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment

@app.get("/job-roles", response_model=List[schemas.JobRoleResponse])
async def get_all_job_roles(db: Session = Depends(get_db)):
    """Get all job roles"""
    roles = db.query(models.JobRole).all()
    return roles

@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get database statistics"""
    total_assessments = db.query(models.Assessment).count()
    total_roles = db.query(models.JobRole).count()
    total_recommendations = db.query(models.Recommendation).count()
    
    return {
        "total_assessments": total_assessments,
        "total_job_roles": total_roles,
        "total_recommendations": total_recommendations,
        "categories": {
            "technical": db.query(models.Assessment).filter(models.Assessment.category == "Technical").count(),
            "cognitive": db.query(models.Assessment).filter(models.Assessment.category == "Cognitive").count(),
            "behavioral": db.query(models.Assessment).filter(models.Assessment.category == "Behavioral").count()
        }
    }

@app.post("/recommend", response_model=schemas.RecommendationResponse)
async def get_recommendations(
    request: schemas.RecommendationRequest,
    db: Session = Depends(get_db)
):
    """Get AI-powered assessment recommendations for a job role"""
    try:
        recommendations = recommendation_engine.recommend(
            job_role=request.job_role,
            top_k=request.top_k
        )
        
        recommended_tests = []
        for rec in recommendations:
            recommended_tests.append(schemas.RecommendedTest(
                test_name=rec['test_name'],
                test_description=rec['test_description'],
                category=rec['category'],
                confidence_score=rec['confidence_score'],
                skills_match=rec['skills_assessed']
            ))
        
        recommendation_record = models.Recommendation(
            job_role=request.job_role,
            recommended_tests=json.dumps([r.test_name for r in recommended_tests]),
            confidence_score=recommended_tests[0].confidence_score if recommended_tests else 0.0
        )
        db.add(recommendation_record)
        db.commit()
        
        return schemas.RecommendationResponse(
            job_role=request.job_role,
            recommendations=recommended_tests,
            total_recommendations=len(recommended_tests),
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation error: {str(e)}")

@app.get("/model-info")
async def get_model_info():
    """Get information about the ML model"""
    return recommendation_engine.get_model_info()


@app.get("/seed-database")
async def seed_database(db: Session = Depends(get_db)):
    """Seed database with sample data"""
    try:
        from ml.data.sample_assessments import SAMPLE_ASSESSMENTS, SAMPLE_JOB_ROLES
        
        existing = db.query(models.Assessment).count()
        if existing > 0:
            return {"status": "already_seeded", "count": existing}
        
        for assessment_data in SAMPLE_ASSESSMENTS:
            db.add(models.Assessment(**assessment_data))
        
        for role_data in SAMPLE_JOB_ROLES:
            db.add(models.JobRole(**role_data))
        
        db.commit()
        recommendation_engine.train(db)
        
        return {
            "status": "success",
            "assessments": len(SAMPLE_ASSESSMENTS),
            "job_roles": len(SAMPLE_JOB_ROLES)
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))