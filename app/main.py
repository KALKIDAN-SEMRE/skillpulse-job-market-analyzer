"""
FastAPI main application file.
Provides API endpoints for the SkillPulse backend.
"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db, init_db
from app.models import JobPost, Skill

# Create FastAPI app
app = FastAPI(
    title="SkillPulse API",
    description="API for analyzing job market skills from Telegram job posts",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup."""
    init_db()
    print("Database initialized")


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "message": "SkillPulse API",
        "version": "1.0.0",
        "endpoints": {
            "jobs": "/jobs",
            "job_by_id": "/jobs/{id}",
            "skills": "/skills",
            "stats": "/stats"
        }
    }


@app.get("/jobs", response_model=List[dict])
async def get_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all job posts with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of job posts with their skills
    """
    jobs = db.query(JobPost).offset(skip).limit(limit).all()
    
    result = []
    for job in jobs:
        result.append({
            "id": job.id,
            "job_title": job.job_title,
            "salary": job.salary,
            "posted_date": job.posted_date.isoformat() if job.posted_date else None,
            "created_at": job.created_at.isoformat() if job.created_at else None,
            "skills": [skill.name for skill in job.skills],
            "raw_text_preview": job.raw_text[:200] + "..." if len(job.raw_text) > 200 else job.raw_text
        })
    
    return result


@app.get("/jobs/{job_id}")
async def get_job(job_id: int, db: Session = Depends(get_db)):
    """
    Get a specific job post by ID.
    
    Args:
        job_id: ID of the job post
        db: Database session
        
    Returns:
        Job post details
    """
    job = db.query(JobPost).filter(JobPost.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job post not found")
    
    return {
        "id": job.id,
        "job_title": job.job_title,
        "salary": job.salary,
        "posted_date": job.posted_date.isoformat() if job.posted_date else None,
        "created_at": job.created_at.isoformat() if job.created_at else None,
        "skills": [skill.name for skill in job.skills],
        "raw_text": job.raw_text
    }


@app.get("/skills", response_model=List[dict])
async def get_skills(db: Session = Depends(get_db)):
    """
    Get all skills with job post counts.
    
    Args:
        db: Database session
        
    Returns:
        List of skills with their usage counts
    """
    skills = db.query(Skill).all()
    
    result = []
    for skill in skills:
        result.append({
            "id": skill.id,
            "name": skill.name,
            "job_count": len(skill.job_posts)
        })
    
    # Sort by job count (most popular first)
    result.sort(key=lambda x: x["job_count"], reverse=True)
    
    return result


@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """
    Get statistics about collected job posts.
    
    Args:
        db: Database session
        
    Returns:
        Statistics dictionary
    """
    total_jobs = db.query(JobPost).count()
    total_skills = db.query(Skill).count()
    jobs_with_salary = db.query(JobPost).filter(JobPost.salary.isnot(None)).count()
    jobs_with_title = db.query(JobPost).filter(JobPost.job_title.isnot(None)).count()
    
    return {
        "total_job_posts": total_jobs,
        "total_skills": total_skills,
        "jobs_with_salary": jobs_with_salary,
        "jobs_with_title": jobs_with_title,
        "jobs_with_salary_percentage": round((jobs_with_salary / total_jobs * 100) if total_jobs > 0 else 0, 2),
        "jobs_with_title_percentage": round((jobs_with_title / total_jobs * 100) if total_jobs > 0 else 0, 2)
    }

