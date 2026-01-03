"""
Telegram collector using Telethon.
Fetches messages from public Telegram channels and stores them.
"""
import asyncio
import os
from datetime import datetime, timedelta
from typing import List, Optional
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import Message
from sqlalchemy.orm import Session

from app.database import SessionLocal, init_db
from app.models import JobPost, Skill
from app.extractor import extract_salary, extract_skills, extract_job_title

# Load environment variables
load_dotenv()

# Telegram API credentials (get from https://my.telegram.org)
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
SESSION_NAME = os.getenv('TELEGRAM_SESSION_NAME', 'skillpulse_session')


def get_or_create_skill(db: Session, skill_name: str) -> Skill:
    """
    Get existing skill or create a new one.
    
    Args:
        db: Database session
        skill_name: Name of the skill
        
    Returns:
        Skill object
    """
    skill = db.query(Skill).filter(Skill.name == skill_name).first()
    if not skill:
        skill = Skill(name=skill_name)
        db.add(skill)
        db.flush()  # Flush to get the ID, but don't commit yet
        db.refresh(skill)
    return skill


def save_job_post(db: Session, raw_text: str, posted_date: datetime, 
                  job_title: Optional[str] = None, salary: Optional[str] = None,
                  skills: Optional[List[str]] = None) -> JobPost:
    """
    Save a job post to the database with extracted data.
    
    Args:
        db: Database session
        raw_text: Original message text
        posted_date: When the message was posted
        job_title: Extracted job title (optional)
        salary: Extracted salary (optional)
        skills: List of skill names (optional)
        
    Returns:
        Created JobPost object
    """
    # Create JobPost
    job_post = JobPost(
        raw_text=raw_text,
        job_title=job_title,
        salary=salary,
        posted_date=posted_date
    )
    
    db.add(job_post)
    db.flush()  # Flush to get the ID
    
    # Add skills if provided
    if skills:
        for skill_name in skills:
            skill = get_or_create_skill(db, skill_name)
            job_post.skills.append(skill)
    
    db.commit()
    db.refresh(job_post)
    
    return job_post


async def collect_from_channel(client: TelegramClient, channel_username: str, 
                               limit: int = 100) -> int:
    """
    Collect job posts from a Telegram channel.
    
    Args:
        client: TelegramClient instance
        channel_username: Username of the channel (without @)
        limit: Maximum number of messages to fetch
        
    Returns:
        Number of job posts saved
    """
    db = SessionLocal()
    saved_count = 0
    
    try:
        print(f"Fetching messages from @{channel_username}...")
        
        # Get messages from the channel
        messages = await client.get_messages(channel_username, limit=limit)
        
        print(f"Found {len(messages)} messages. Processing...")
        
        for message in messages:
            # Skip if message has no text
            if not message.text or not message.text.strip():
                continue
            
            raw_text = message.text
            
            # Extract data
            salary = extract_salary(raw_text)
            skills_set = extract_skills(raw_text)
            job_title = extract_job_title(raw_text)
            
            # Convert skills set to list
            skills_list = list(skills_set) if skills_set else None
            
            # Check if this message already exists (simple duplicate check)
            # In a production system, you'd use message.id or a hash
            existing = db.query(JobPost).filter(
                JobPost.raw_text == raw_text,
                JobPost.posted_date == message.date
            ).first()
            
            if existing:
                continue  # Skip duplicates
            
            # Save to database
            save_job_post(
                db=db,
                raw_text=raw_text,
                posted_date=message.date,
                job_title=job_title,
                salary=salary,
                skills=skills_list
            )
            
            saved_count += 1
            
            if saved_count % 10 == 0:
                print(f"  Saved {saved_count} job posts...")
    
    except Exception as e:
        print(f"Error collecting from @{channel_username}: {e}")
        db.rollback()
    finally:
        db.close()
    
    return saved_count


async def collect_jobs(channel_usernames: List[str], messages_per_channel: int = 100):
    """
    Main function to collect job posts from multiple Telegram channels.
    
    Args:
        channel_usernames: List of channel usernames (without @)
        messages_per_channel: Number of messages to fetch per channel
    """
    if not API_ID or not API_HASH:
        raise ValueError(
            "TELEGRAM_API_ID and TELEGRAM_API_HASH must be set in .env file. "
            "Get them from https://my.telegram.org"
        )
    
    # Initialize database (create tables if they don't exist)
    init_db()
    
    # Create Telegram client
    client = TelegramClient(SESSION_NAME, int(API_ID), API_HASH)
    
    try:
        # Connect to Telegram
        print("Connecting to Telegram...")
        await client.start()
        print("Connected successfully!")
        
        total_saved = 0
        
        # Collect from each channel
        for channel in channel_usernames:
            try:
                count = await collect_from_channel(client, channel, messages_per_channel)
                total_saved += count
                print(f"Saved {count} job posts from @{channel}\n")
            except Exception as e:
                print(f"Failed to collect from @{channel}: {e}\n")
                continue
        
        print(f"Collection complete! Total job posts saved: {total_saved}")
    
    finally:
        await client.disconnect()
        print("Disconnected from Telegram")


def run_collector(channel_usernames: List[str], messages_per_channel: int = 100):
    """
    Synchronous wrapper to run the async collector.
    
    Args:
        channel_usernames: List of channel usernames (without @)
        messages_per_channel: Number of messages to fetch per channel
    """
    asyncio.run(collect_jobs(channel_usernames, messages_per_channel))

