# SkillPulse - Job Market Analyzer

**Day 1: Data Collection and Storage**

SkillPulse analyzes public Telegram job posts to identify in-demand and high-paying tech skills.

## Project Structure

```
skillpulse-job-market-analyzer/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application
│   ├── database.py          # SQLAlchemy database configuration
│   ├── models.py            # Database models (JobPost, Skill, JobSkill)
│   ├── collector.py         # Telegram collector using Telethon
│   └── extractor.py         # Data extraction logic (salary, skills, job title)
├── run_collector.py         # Script to run the data collector
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── README.md               # This file
└── skillpulse.db          # SQLite database (created automatically)
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Telegram API Credentials

1. Go to https://my.telegram.org/apps
2. Log in with your phone number
3. Create a new application
4. Copy your `api_id` and `api_hash`

### 3. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```
   (On Linux/Mac: `cp .env.example .env`)

2. Edit `.env` and add your credentials:
   ```
   TELEGRAM_API_ID=your_api_id_here
   TELEGRAM_API_HASH=your_api_hash_here
   ```

### 4. Initialize Database

The database will be created automatically when you first run the FastAPI app or the collector.

## Running the Application

### Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

### Run the Data Collector

1. Edit `run_collector.py` and add Telegram channel usernames to the `TELEGRAM_CHANNELS` list:
   ```python
   TELEGRAM_CHANNELS = [
       "channel_username_1",
       "channel_username_2",
   ]
   ```
   (Use channel usernames without the @ symbol)

2. Run the collector:
   ```bash
   python run_collector.py
   ```

3. On first run, you'll be prompted to:
   - Enter your phone number
   - Enter the verification code sent to Telegram
   - The session will be saved for future runs

## API Endpoints

### GET `/`
Root endpoint with API information.

### GET `/jobs`
Get all job posts (paginated).
- Query parameters:
  - `skip`: Number of records to skip (default: 0)
  - `limit`: Maximum records to return (default: 100)

### GET `/jobs/{job_id}`
Get a specific job post by ID.

### GET `/skills`
Get all skills with job post counts (sorted by popularity).

### GET `/stats`
Get statistics about collected job posts.

## Database Models

### JobPost
- `id`: Primary key
- `raw_text`: Original message text from Telegram
- `job_title`: Extracted job title
- `salary`: Extracted salary information
- `posted_date`: When the job was posted on Telegram
- `created_at`: When the record was created in our database

### Skill
- `id`: Primary key
- `name`: Skill name (unique, e.g., "Python", "React")

### JobSkill (Many-to-Many)
- Links JobPost and Skill tables
- Created automatically by SQLAlchemy

## Data Extraction

The system extracts:
1. **Salary**: Using regex patterns to find salary ranges and amounts
2. **Skills**: Using a predefined keyword list of tech skills
3. **Job Title**: Basic inference from common patterns in job posts

## Day 1 Deliverables

✅ FastAPI backend skeleton  
✅ SQLite database with SQLAlchemy  
✅ Database models (JobPost, Skill, JobSkill)  
✅ Telegram collector using Telethon  
✅ Data extraction (salary, skills, job title)  
✅ API endpoints for viewing data  
✅ Instructions for running locally  

## Notes

- The database file (`skillpulse.db`) will be created in the project root
- First-time Telegram authentication requires your phone number and verification code
- The session file (e.g., `skillpulse_session.session`) is saved locally for future runs
- Duplicate messages are skipped based on text content and date

## Next Steps (Future Days)

- ML-based skill extraction
- Salary normalization and analysis
- Trend analysis and forecasting
- Frontend dashboard
- More sophisticated job title extraction

