"""
Database models for SkillPulse.
Defines the schema for JobPost, Skill, and their relationship.
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Table, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# Association table for many-to-many relationship between JobPost and Skill
job_skill_association = Table(
    'job_skill',
    Base.metadata,
    Column('job_post_id', Integer, ForeignKey('job_posts.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True)
)


class JobPost(Base):
    """
    Model representing a job posting from Telegram.
    Stores raw text and extracted structured data.
    """
    __tablename__ = "job_posts"

    id = Column(Integer, primary_key=True, index=True)
    raw_text = Column(Text, nullable=False, comment="Original text from Telegram message")
    job_title = Column(String(255), nullable=True, comment="Extracted or inferred job title")
    salary = Column(String(100), nullable=True, comment="Extracted salary information")
    posted_date = Column(DateTime, nullable=False, comment="Date when the job was posted on Telegram")
    created_at = Column(DateTime, server_default=func.now(), comment="When this record was created in our DB")
    
    # Many-to-many relationship with Skill
    skills = relationship("Skill", secondary=job_skill_association, back_populates="job_posts")


class Skill(Base):
    """
    Model representing a technical skill.
    Used in many-to-many relationship with JobPost.
    """
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True, comment="Name of the skill (e.g., 'Python', 'React')")
    
    # Many-to-many relationship with JobPost
    job_posts = relationship("JobPost", secondary=job_skill_association, back_populates="skills")

