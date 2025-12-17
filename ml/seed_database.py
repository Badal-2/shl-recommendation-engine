import sys
sys.path.append('.')

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Assessment, JobRole, Base
from ml.data.sample_assessments import SAMPLE_ASSESSMENTS, SAMPLE_JOB_ROLES

def seed_assessments(db: Session):
    """Add sample assessments to database"""
    print("Seeding assessments...")
    
    # Check if data already exists
    existing_count = db.query(Assessment).count()
    if existing_count > 0:
        print(f"Database already has {existing_count} assessments. Skipping...")
        return
    
    # Add assessments
    for assessment_data in SAMPLE_ASSESSMENTS:
        assessment = Assessment(**assessment_data)
        db.add(assessment)
    
    db.commit()
    print(f"✅ Added {len(SAMPLE_ASSESSMENTS)} assessments!")

def seed_job_roles(db: Session):
    """Add sample job roles to database"""
    print("Seeding job roles...")
    
    # Check if data already exists
    existing_count = db.query(JobRole).count()
    if existing_count > 0:
        print(f"Database already has {existing_count} job roles. Skipping...")
        return
    
    # Add job roles
    for role_data in SAMPLE_JOB_ROLES:
        role = JobRole(**role_data)
        db.add(role)
    
    db.commit()
    print(f"✅ Added {len(SAMPLE_JOB_ROLES)} job roles!")

def main():
    """Main seeding function"""
    print("🌱 Starting database seeding...\n")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Seed data
        seed_assessments(db)
        seed_job_roles(db)
        
        print("\n✅ Database seeding completed successfully!")
        
        # Show summary
        total_assessments = db.query(Assessment).count()
        total_roles = db.query(JobRole).count()
        
        print(f"\n📊 Database Summary:")
        print(f"   - Total Assessments: {total_assessments}")
        print(f"   - Total Job Roles: {total_roles}")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()