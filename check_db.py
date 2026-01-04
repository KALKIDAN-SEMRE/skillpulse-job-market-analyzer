"""
Script to check database contents.
Usage: python check_db.py
"""
from app.database import SessionLocal, init_db
from app.models import JobPost, Skill

# Initialize database (creates tables if they don't exist)
init_db()

db = SessionLocal()

try:
    total_jobs = db.query(JobPost).count()
    total_skills = db.query(Skill).count()
    jobs_with_salary = db.query(JobPost).filter(JobPost.salary.isnot(None)).count()
    jobs_with_title = db.query(JobPost).filter(JobPost.job_title.isnot(None)).count()
    
    print("=" * 50)
    print("📊 Database Statistics")
    print("=" * 50)
    print(f"Total job posts: {total_jobs}")
    print(f"Total skills: {total_skills}")
    print(f"Jobs with salary: {jobs_with_salary} ({jobs_with_salary/total_jobs*100:.1f}%)" if total_jobs > 0 else "Jobs with salary: 0")
    print(f"Jobs with title: {jobs_with_title} ({jobs_with_title/total_jobs*100:.1f}%)" if total_jobs > 0 else "Jobs with title: 0")
    
    if total_skills > 0:
        print("\n" + "=" * 50)
        print("🔝 Top 10 Skills by Frequency")
        print("=" * 50)
        from sqlalchemy import func
        top_skills = db.query(
            Skill.name,
            func.count(JobPost.id).label('job_count')
        ).join(
            Skill.job_posts
        ).group_by(Skill.id).order_by(func.count(JobPost.id).desc()).limit(10).all()
        
        for skill_name, count in top_skills:
            print(f"  {skill_name}: {count} jobs")
    
    if total_jobs == 0:
        print("\n⚠️  Database is empty. Run the collector to fetch job posts:")
        print("   python run_collector.py")
    
finally:
    db.close()
