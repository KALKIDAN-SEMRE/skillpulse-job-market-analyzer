# SkillPulse — Job Market Analyzer

SkillPulse collects public Telegram job posts and extracts structured insights (job titles, salaries, and skills) to help identify in-demand and high-paying technical skills.

## Quick Start

1. Clone the repo and enter the folder:

```bash
git clone <repository-url>
cd skillpulse-job-market-analyzer
```

2. Create and activate a virtual environment:

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure Telegram credentials by copying `.env.example` to `.env` and filling `TELEGRAM_API_ID` and `TELEGRAM_API_HASH`.

5. Run the collector or API server as needed (examples below).

## Typical Workflows

- Run the Telegram collector (fill channels in `run_collector.py` first):

```bash
python run_collector.py
```

- Start the API (development):

```bash
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

## Configuration

- Environment: copy `.env.example` to `.env` and set `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, and `TELEGRAM_SESSION_NAME`.
- Do not commit `.env` to source control.

## Project Layout

Top-level files you will use often:

- `run_collector.py` — run the Telegram collection job
- `check_db.py` — quick DB stats and sanity checks
- `test_day1.py` — basic verification tests for this stage
- `requirements.txt` — pinned Python dependencies
- `skillpulse_session.session` — Telegram session created after first auth

Key package: `app/` contains the FastAPI app, ORM models, collector and extractor logic.

## Data Extraction Summary

SkillPulse extracts:

- Salary information (regex-based patterns: `$100k/year`, `50k-80k`, etc.)
- Skills (from a curated keyword list)
- Job titles (simple pattern inference)

Extracted data is stored in SQLite (`skillpulse.db`) via SQLAlchemy models.

## Useful Commands

- Run tests / verification:

```bash
python test_day1.py
```

- Inspect database with sqlite3:

```bash
sqlite3 skillpulse.db
.tables
SELECT COUNT(*) FROM job_posts;
```

## Troubleshooting (Common Issues)

- Missing dependency error: ensure virtualenv is activated and run `pip install -r requirements.txt`.
- `TELEGRAM_API_ID` missing: ensure `.env` exists and contains valid values.
- Collector authentication: delete `skillpulse_session.session` and re-authenticate if needed.
- No posts collected: confirm channels in `run_collector.py` are public and have job posts; increase `MESSAGES_PER_CHANNEL`.

## Next Steps

- Add more extraction patterns and improve title/skill normalization.
- Create small sample dataset and unit tests for extraction functions.

---

If you'd like, I can also:

- expand the Usage section with explicit examples for `run_collector.py` parameters,
- add a minimal CONTRIBUTING guide, or
- run the tests and report results.

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
