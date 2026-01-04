# SkillPulse - Job Market Analyzer

**Day 1: Data Collection and Storage**

SkillPulse analyzes public Telegram job posts to identify in-demand and high-paying tech skills.

## 📋 Table of Contents

- [Requirements](#-requirements)
- [Project Structure](#-project-structure)
- [Setup Instructions](#-setup-instructions)
- [Running the Application](#-running-the-application)
- [API Endpoints](#-api-endpoints)
- [Database Models](#-database-models)
- [Troubleshooting](#-troubleshooting)

---

## 🎯 Requirements

### Python Version
- **Python 3.11+** is required
- Check your Python version:
  ```bash
  python --version
  ```

### System Requirements
- Internet connection (for Telegram API)
- SQLite (comes built-in with Python)
- Git (for cloning the repository)

---

## 📁 Project Structure

```
skillpulse-job-market-analyzer/
│
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application
│   ├── database.py          # SQLAlchemy database configuration
│   ├── models.py            # Database models (JobPost, Skill, JobSkill)
│   ├── collector.py         # Telegram collector using Telethon
│   └── extractor.py         # Data extraction logic (salary, skills, job title)
│
├── venv/                    # Virtual environment (created during setup)
├── .env                     # Environment variables (create from .env.example)
├── .env.example             # Environment variables template
├── requirements.txt         # Python dependencies
├── run_collector.py         # Script to run the data collector
├── check_db.py              # Script to check database statistics
├── test_day1.py             # Day 1 verification test script
├── skillpulse.db            # SQLite database (created automatically)
├── skillpulse_session.session  # Telegram session file (created after first login)
└── README.md                # This file
```

---

## 🚀 Setup Instructions

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd skillpulse-job-market-analyzer
```

### Step 2: Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt, indicating the virtual environment is active.

> **Note:** Always activate the virtual environment before working on the project.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages:
- `fastapi` - Web framework for building APIs
- `uvicorn` - ASGI server to run FastAPI
- `sqlalchemy` - SQL toolkit and ORM
- `telethon` - Telegram client library
- `python-dotenv` - Load environment variables from .env file
- `pydantic` - Data validation (required by FastAPI)

### Step 4: Get Telegram API Credentials

1. Go to [https://my.telegram.org/apps](https://my.telegram.org/apps)
2. Log in with your phone number
3. Create a new application (if you don't have one)
4. Copy your `api_id` and `api_hash`

### Step 5: Configure Environment Variables

1. **Create `.env` file** in the project root:

   **Windows:**
   ```bash
   copy .env.example .env
   ```

   **Linux/Mac:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env`** and add your Telegram credentials:
   ```dotenv
   TELEGRAM_API_ID=your_api_id_here
   TELEGRAM_API_HASH=your_api_hash_here
   TELEGRAM_SESSION_NAME=skillpulse_session
   ```

   Replace `your_api_id_here` and `your_api_hash_here` with your actual credentials.

> **⚠️ Important:** Never commit `.env` file to Git! It should already be in `.gitignore`.

### Step 6: Initialize Database

The database will be created automatically when you:
- Run the FastAPI server for the first time, OR
- Run the collector script for the first time

The database file `skillpulse.db` will be created in the project root.

---

## 🏃 Running the Application

### Start FastAPI Server (Backend API)

```bash
uvicorn app.main:app --reload
```

The `--reload` flag enables auto-reload on code changes (useful for development).

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
Database initialized
INFO:     Application startup complete.
```

**Access the API:**
- **API Documentation (Swagger UI):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc
- **Root Endpoint:** http://localhost:8000/

### Run the Data Collector

1. **Edit `run_collector.py`** and add Telegram channel usernames:
   ```python
   TELEGRAM_CHANNELS = [
       "channel_username_1",  # Without @ symbol
       "channel_username_2",
       "channel_username_3",
   ]
   ```

   > **Note:** Use channel usernames **without the @ symbol**. Channels must be public.

2. **Run the collector:**
   ```bash
   python run_collector.py
   ```

3. **First-time authentication:**
   - You'll be prompted to enter your phone number
   - Enter the verification code sent to Telegram
   - The session will be saved in `skillpulse_session.session` for future runs

**Expected Output:**
```
===================================
🚀 SkillPulse Telegram Collector
===================================

Channels to collect from: ['channel1', 'channel2']
Messages per channel: 100

Connecting to Telegram...
Connected successfully!
Fetching messages from @channel1...
Found 100 messages. Processing...
  Saved 10 job posts...
  Saved 20 job posts...
Saved 85 job posts from @channel1

Collection complete! Total job posts saved: 85
```

### Check Database Statistics

```bash
python check_db.py
```

This will display:
- Total number of job posts
- Total number of unique skills
- Jobs with salary information
- Jobs with job titles
- Top 10 most frequent skills

---

## 🔌 API Endpoints

### GET `/`
Root endpoint with API information.

**Example Response:**
```json
{
  "message": "SkillPulse API",
  "version": "1.0.0",
  "endpoints": {
    "jobs": "/jobs",
    "job_by_id": "/jobs/{id}",
    "skills": "/skills",
    "stats": "/stats"
  }
}
```

### GET `/jobs`
Get all job posts (paginated).

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 100)

**Example:**
```
GET http://localhost:8000/jobs?skip=0&limit=50
```

### GET `/jobs/{job_id}`
Get a specific job post by ID.

**Example:**
```
GET http://localhost:8000/jobs/1
```

### GET `/skills`
Get all skills with job post counts (sorted by popularity).

**Example:**
```
GET http://localhost:8000/skills
```

### GET `/stats`
Get statistics about collected job posts.

**Example Response:**
```json
{
  "total_job_posts": 150,
  "total_skills": 45,
  "jobs_with_salary": 120,
  "jobs_with_title": 140,
  "jobs_with_salary_percentage": 80.0,
  "jobs_with_title_percentage": 93.33
}
```

---

## 🗄️ Database Models

### JobPost
- `id` - Primary key
- `raw_text` - Original message text from Telegram
- `job_title` - Extracted job title
- `salary` - Extracted salary information
- `posted_date` - When the job was posted on Telegram
- `created_at` - When the record was created in our database

### Skill
- `id` - Primary key
- `name` - Skill name (unique, e.g., "Python", "React")

### JobSkill (Association Table)
- Links JobPost and Skill tables (many-to-many relationship)
- Created automatically by SQLAlchemy

### Accessing the Database

You can use SQLite command-line tool to inspect the database:

```bash
sqlite3 skillpulse.db
```

**Useful SQLite commands:**
```sql
.tables                    -- List all tables
.schema job_posts          -- Show table structure
SELECT COUNT(*) FROM job_posts;  -- Count job posts
SELECT * FROM job_posts LIMIT 5; -- View sample data
.exit                      -- Exit SQLite
```

---

## 🔍 Data Extraction

The system extracts three types of information from job posts:

1. **Salary**: Using regex patterns to find salary ranges and amounts
   - Patterns: `$50,000 - $80,000`, `50k-80k`, `$100k/year`, etc.

2. **Skills**: Using a predefined keyword list of tech skills
   - Examples: Python, JavaScript, React, Django, AWS, Docker, etc.

3. **Job Title**: Basic inference from common patterns
   - Patterns: "Looking for a Senior Python Developer", "Hiring: Backend Engineer", etc.

---

## 🧪 Testing

### Run Day 1 Verification Tests

```bash
python test_day1.py
```

This script checks:
- ✅ Project structure
- ✅ Environment setup
- ✅ Database setup
- ✅ FastAPI initialization
- ✅ Data extraction functions
- ✅ Database data (if exists)
- ✅ README quality

---

## ❓ Troubleshooting

### Issue: "No module named 'sqlalchemy'" or similar

**Solution:** Make sure you've activated the virtual environment and installed dependencies:
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Issue: "TELEGRAM_API_ID not set" error

**Solution:** 
1. Make sure `.env` file exists in the project root
2. Check that `.env` contains `TELEGRAM_API_ID` and `TELEGRAM_API_HASH`
3. Verify there are no extra spaces or quotes around the values

### Issue: Collector fails with authentication errors

**Solution:**
1. Verify your API_ID and API_HASH are correct
2. Delete the session file (`skillpulse_session.session`) and try again
3. Make sure you're using the correct phone number format (with country code, e.g., +1234567890)

### Issue: "No job posts collected" or "Saved 0 job posts"

**Solution:**
1. Verify channel names in `run_collector.py` are correct (without @)
2. Make sure channels are public and accessible
3. Check that channels actually have job posts
4. Increase `MESSAGES_PER_CHANNEL` in `run_collector.py`

### Issue: Database file not created

**Solution:** 
- Run FastAPI server or collector once to initialize the database:
  ```bash
  uvicorn app.main:app --reload
  # OR
  python run_collector.py
  ```

### Issue: Port 8000 already in use

**Solution:** Use a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

---

## 📝 Important Notes

### Environment Safety
- **Never commit `.env` file** to Git (it should be in `.gitignore`)
- **Never commit `.session` files** (contains authentication tokens)
- **Never commit `skillpulse.db`** if it contains real data (add to `.gitignore`)

### Telegram Session
- First-time login creates a session file (e.g., `skillpulse_session.session`)
- This file stores your authentication, so you won't need to enter credentials again
- Keep this file secure and don't share it

### Database Backup
- The database file `skillpulse.db` contains all collected data
- Consider backing it up periodically:
  ```bash
  copy skillpulse.db skillpulse_backup.db  # Windows
  cp skillpulse.db skillpulse_backup.db    # Linux/Mac
  ```

### Data Collection
- Only messages with text content are saved
- Duplicate messages (same text and date) are skipped
- Data extraction (salary, skills, title) happens automatically

---

## ✅ Day 1 Deliverables

- ✅ FastAPI backend skeleton
- ✅ SQLite database with SQLAlchemy
- ✅ Database models (JobPost, Skill, JobSkill)
- ✅ Telegram collector using Telethon
- ✅ Data extraction (salary, skills, job title)
- ✅ API endpoints for viewing data
- ✅ Comprehensive documentation

---

## 🚀 Next Steps (Future Days)

- ML-based skill extraction
- Salary normalization and analysis
- Trend analysis and forecasting
- Frontend dashboard
- More sophisticated job title extraction
- Real-time data updates

---

## 📄 License

[Add your license here]

## 👥 Contributing

[Add contributing guidelines here]

## 📧 Contact

[Add contact information here]
