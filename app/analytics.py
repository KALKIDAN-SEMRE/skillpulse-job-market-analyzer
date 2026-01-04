"""
Analytics engine for SkillPulse.
Uses pandas to analyze job post data and compute insights.
"""
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import SessionLocal
from app.models import JobPost, Skill


def parse_salary(salary_str: str) -> Optional[float]:
    """
    Parse salary string to extract numeric value (average if range).
    
    Handles formats like:
    - "55,000 - 70,000" -> 62500 (average)
    - "1,400 USD" -> 1400
    - "50k-80k" -> 65000 (average)
    - "100k" -> 100000
    
    Args:
        salary_str: Salary string from database
        
    Returns:
        Numeric salary value or None if cannot parse
    """
    if not salary_str:
        return None
    
    # Remove currency symbols and common words
    text = salary_str.upper().replace('Birr', '').replace('USD', '')
    text = text.replace('PER YEAR', '').replace('/YEAR', '').replace('ANNUALLY', '')
    text = text.replace('$', '').strip()
    
    # Extract numbers with optional 'k' suffix (handles ranges like "50000-80000" or "50k-80k")
    # Pattern matches: digits (with commas), optional 'k', separated by dash/hyphen
    pattern = r'(\d{1,3}(?:,\d{3})*)\s*(k?)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    if not matches:
        return None
    
    # Convert to floats, handling 'k' suffix (thousands) and commas
    values = []
    for num_str, k_suffix in matches:
        # Remove commas and convert to float
        num = float(num_str.replace(',', ''))
        # Multiply by 1000 if 'k' suffix present
        if k_suffix.lower() == 'k':
            num *= 1000
        values.append(num)
    
    # Return average if range, single value otherwise
    return sum(values) / len(values) if values else None


# Note: pandas is imported but current implementation uses SQLAlchemy queries
# directly for better performance. pandas can be used for more complex analysis
# if needed in the future.


def top_skills_week(db: Session = None, limit: int = 10) -> List[Dict]:
    """
    Get top skills from jobs posted in the last 7 days.
    
    Args:
        db: Database session (creates new one if not provided)
        limit: Number of top skills to return
        
    Returns:
        List of dicts with keys: skill_name, job_count, avg_salary
    """
    if db is None:
        db = SessionLocal()
        close_db = True
    else:
        close_db = False
    
    try:
        # Get jobs from last 7 days
        cutoff_date = datetime.now() - timedelta(days=7)
        
        # Query skills with job counts for last 7 days
        results = db.query(
            Skill.name,
            func.count(JobPost.id).label('job_count')
        ).join(
            Skill.job_posts
        ).filter(
            JobPost.posted_date >= cutoff_date
        ).group_by(
            Skill.id
        ).order_by(
            func.count(JobPost.id).desc()
        ).limit(limit).all()
        
        # Get average salary per skill
        top_skills = []
        for skill_name, job_count in results:
            # Get average salary for this skill in last 7 days
            jobs_with_skill = db.query(JobPost).join(
                JobPost.skills
            ).filter(
                Skill.name == skill_name,
                JobPost.posted_date >= cutoff_date,
                JobPost.salary.isnot(None)
            ).all()
            
            salaries = []
            for job in jobs_with_skill:
                parsed = parse_salary(job.salary)
                if parsed:
                    salaries.append(parsed)
            
            avg_salary = sum(salaries) / len(salaries) if salaries else None
            
            top_skills.append({
                'skill_name': skill_name,
                'job_count': job_count,
                'avg_salary': avg_salary
            })
        
        return top_skills
    
    finally:
        if close_db:
            db.close()


def top_skills_month(db: Session = None, limit: int = 10) -> List[Dict]:
    """
    Get top skills from jobs posted in the last 30 days.
    
    Args:
        db: Database session (creates new one if not provided)
        limit: Number of top skills to return
        
    Returns:
        List of dicts with keys: skill_name, job_count, avg_salary
    """
    if db is None:
        db = SessionLocal()
        close_db = True
    else:
        close_db = False
    
    try:
        # Get jobs from last 30 days
        cutoff_date = datetime.now() - timedelta(days=30)
        
        # Query skills with job counts for last 30 days
        results = db.query(
            Skill.name,
            func.count(JobPost.id).label('job_count')
        ).join(
            Skill.job_posts
        ).filter(
            JobPost.posted_date >= cutoff_date
        ).group_by(
            Skill.id
        ).order_by(
            func.count(JobPost.id).desc()
        ).limit(limit).all()
        
        # Get average salary per skill
        top_skills = []
        for skill_name, job_count in results:
            # Get average salary for this skill in last 30 days
            jobs_with_skill = db.query(JobPost).join(
                JobPost.skills
            ).filter(
                Skill.name == skill_name,
                JobPost.posted_date >= cutoff_date,
                JobPost.salary.isnot(None)
            ).all()
            
            salaries = []
            for job in jobs_with_skill:
                parsed = parse_salary(job.salary)
                if parsed:
                    salaries.append(parsed)
            
            avg_salary = sum(salaries) / len(salaries) if salaries else None
            
            top_skills.append({
                'skill_name': skill_name,
                'job_count': job_count,
                'avg_salary': avg_salary
            })
        
        return top_skills
    
    finally:
        if close_db:
            db.close()


def average_salary_per_skill(db: Session = None) -> List[Dict]:
    """
    Calculate average salary for each skill (all time data).
    
    Args:
        db: Database session (creates new one if not provided)
        
    Returns:
        List of dicts with keys: skill_name, avg_salary, job_count
    """
    if db is None:
        db = SessionLocal()
        close_db = True
    else:
        close_db = False
    
    try:
        # Get all skills
        skills = db.query(Skill).all()
        
        results = []
        for skill in skills:
            # Get all jobs with this skill that have salary
            jobs = db.query(JobPost).join(
                JobPost.skills
            ).filter(
                Skill.id == skill.id,
                JobPost.salary.isnot(None)
            ).all()
            
            if not jobs:
                continue
            
            # Parse salaries
            salaries = []
            for job in jobs:
                parsed = parse_salary(job.salary)
                if parsed:
                    salaries.append(parsed)
            
            if salaries:
                avg_salary = sum(salaries) / len(salaries)
                results.append({
                    'skill_name': skill.name,
                    'avg_salary': avg_salary,
                    'job_count': len(jobs)
                })
        
        # Sort by average salary descending
        results.sort(key=lambda x: x['avg_salary'], reverse=True)
        
        return results
    
    finally:
        if close_db:
            db.close()


def top_paying_skills(db: Session = None, limit: int = 10) -> List[Dict]:
    """
    Get top paying skills (highest average salary).
    
    Args:
        db: Database session (creates new one if not provided)
        limit: Number of top skills to return
        
    Returns:
        List of dicts with keys: skill_name, avg_salary, job_count
    """
    all_skills = average_salary_per_skill(db=db)
    return all_skills[:limit]


def get_skill_info(skill_name: str, db: Session = None) -> Optional[Dict]:
    """
    Get detailed information about a specific skill.
    
    Args:
        skill_name: Name of the skill to query
        db: Database session (creates new one if not provided)
        
    Returns:
        Dict with keys: skill_name, total_jobs, avg_salary, jobs_last_7_days, jobs_last_30_days
        or None if skill not found
    """
    if db is None:
        db = SessionLocal()
        close_db = True
    else:
        close_db = False
    
    try:
        # Find skill by name (case-insensitive)
        skill = db.query(Skill).filter(
            func.lower(Skill.name) == skill_name.lower()
        ).first()
        
        if not skill:
            return None
        
        # Get all jobs with this skill
        all_jobs = db.query(JobPost).join(
            JobPost.skills
        ).filter(Skill.id == skill.id).all()
        
        # Get jobs in last 7 days
        cutoff_7d = datetime.now() - timedelta(days=7)
        jobs_7d = [j for j in all_jobs if j.posted_date >= cutoff_7d]
        
        # Get jobs in last 30 days
        cutoff_30d = datetime.now() - timedelta(days=30)
        jobs_30d = [j for j in all_jobs if j.posted_date >= cutoff_30d]
        
        # Calculate average salary
        jobs_with_salary = [j for j in all_jobs if j.salary]
        salaries = []
        for job in jobs_with_salary:
            parsed = parse_salary(job.salary)
            if parsed:
                salaries.append(parsed)
        
        avg_salary = sum(salaries) / len(salaries) if salaries else None
        
        return {
            'skill_name': skill.name,
            'total_jobs': len(all_jobs),
            'avg_salary': avg_salary,
            'jobs_last_7_days': len(jobs_7d),
            'jobs_last_30_days': len(jobs_30d)
        }
    
    finally:
        if close_db:
            db.close()

