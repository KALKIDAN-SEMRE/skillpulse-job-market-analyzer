# Day 2: Analytics & Telegram Bot Setup Guide

This guide covers setting up and running the Day 2 features: Analytics Engine and Telegram Bot.

## 📦 New Dependencies

Day 2 adds two new dependencies:
- `pandas` - For data analysis (though current implementation uses SQLAlchemy for efficiency)
- `python-telegram-bot` - For the Telegram bot

## 🚀 Quick Start

### 1. Install New Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `pandas==2.1.4`
- `python-telegram-bot==20.7`

### 2. Get Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow instructions to create a bot
4. Copy the bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 3. Update `.env` File

Add your bot token to `.env`:

```dotenv
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_SESSION_NAME=skillpulse_session
```

### 4. Run the Bot

```bash
python run_bot.py
```

You should see:
```
==================================================
🤖 SkillPulse Telegram Bot
==================================================

Starting bot...
Press Ctrl+C to stop
```

### 5. Test the Bot

1. Open Telegram and search for your bot (the username you set with BotFather)
2. Start a conversation with `/start`
3. Try the commands:
   - `/top_skills_week` - Top skills in last 7 days
   - `/top_skills_month` - Top skills in last 30 days
   - `/top_paying_skills` - Highest paying skills
   - `/skill Python` - Info about Python skill

## 📊 Analytics Functions

All analytics functions are in `app/analytics.py`:

### Available Functions

1. **`top_skills_week(db=None, limit=10)`**
   - Returns top skills from last 7 days
   - Returns: List of dicts with `skill_name`, `job_count`, `avg_salary`

2. **`top_skills_month(db=None, limit=10)`**
   - Returns top skills from last 30 days
   - Returns: List of dicts with `skill_name`, `job_count`, `avg_salary`

3. **`top_paying_skills(db=None, limit=10)`**
   - Returns skills with highest average salary
   - Returns: List of dicts with `skill_name`, `avg_salary`, `job_count`

4. **`get_skill_info(skill_name, db=None)`**
   - Get detailed info about a specific skill
   - Returns: Dict with `skill_name`, `total_jobs`, `avg_salary`, `jobs_last_7_days`, `jobs_last_30_days`

5. **`average_salary_per_skill(db=None)`**
   - Calculate average salary for all skills
   - Returns: List of dicts sorted by average salary

### Usage Example

```python
from app.analytics import top_skills_week, get_skill_info

# Get top skills from last week
top_skills = top_skills_week(limit=5)
for skill in top_skills:
    print(f"{skill['skill_name']}: {skill['job_count']} jobs")

# Get info about Python
python_info = get_skill_info("Python")
print(f"Python: {python_info['total_jobs']} total jobs")
```

## 🤖 Bot Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Show welcome message and available commands | `/start` |
| `/top_skills_week` | Top skills in last 7 days | `/top_skills_week` |
| `/top_skills_month` | Top skills in last 30 days | `/top_skills_month` |
| `/top_paying_skills` | Highest paying skills | `/top_paying_skills` |
| `/skill <name>` | Get info about a specific skill | `/skill Python` |

## 🔧 Troubleshooting

### Bot doesn't start

**Error:** `TELEGRAM_BOT_TOKEN must be set`

**Solution:** Make sure `.env` file contains `TELEGRAM_BOT_TOKEN=your_token_here`

### Bot doesn't respond

**Check:**
1. Bot is running (check terminal output)
2. Bot token is correct
3. You started the conversation with `/start`
4. Database has data (run collector first if needed)

### No data returned

**Solution:** 
- Run the collector first to populate the database:
  ```bash
  python run_collector.py
  ```

### Salary parsing errors

The salary parser handles common formats but may miss unusual ones. Check `app/analytics.py` `parse_salary()` function to add more patterns if needed.

## 📝 Code Structure

```
app/
├── analytics.py    # Analytics engine (Day 2)
├── bot.py          # Telegram bot (Day 2)
├── collector.py    # Data collector (Day 1)
├── database.py     # Database config (Day 1)
├── extractor.py    # Data extraction (Day 1)
├── main.py         # FastAPI API (Day 1)
└── models.py       # Database models (Day 1)

run_bot.py          # Script to run the bot (Day 2)
```

## ✅ Day 2 Checklist

- [x] Analytics module created
- [x] Top skills (7 days) function
- [x] Top skills (30 days) function
- [x] Average salary per skill function
- [x] Top paying skills function
- [x] Skill info function
- [x] Telegram bot created
- [x] All bot commands implemented
- [x] Bot responds with formatted messages
- [x] Dependencies updated
- [x] Run script created

## 🎯 Next Steps

After Day 2 is working:
- Test all commands with real data
- Verify analytics accuracy
- Consider adding more commands or analytics
- Prepare for Day 3 (if applicable)

