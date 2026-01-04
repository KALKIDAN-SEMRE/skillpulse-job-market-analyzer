"""
SkillPulse Telegram Bot (Professional Version)
Provides analytics insights with buttons, charts, skill selection, and references.

Author: Your Name
Reference: Job data collected from public Telegram job channels via Telethon collector
"""

import os
import logging
from io import BytesIO
from datetime import datetime, timedelta
from dotenv import load_dotenv
import matplotlib.pyplot as plt

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes
)

from app.analytics import (
    top_skills_week,
    top_skills_month,
    top_paying_skills,
    get_skill_info,
    get_all_skills  # New helper to list all skills
)

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Helper functions --- #

def format_currency(amount: float) -> str:
    """Format numeric amount as currency string."""
    return f"{amount:,.0f} ETB"

def create_bar_chart(data, title: str, value_key: str = "job_count") -> BytesIO:
    """Generate a horizontal bar chart and return as BytesIO."""
    if not data:
        return None
    names = [d['skill_name'] for d in data]
    values = [d[value_key] for d in data]
    plt.figure(figsize=(8, 5))
    plt.barh(names[::-1], values[::-1], color="#4CAF50")
    plt.title(title)
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()
    return buffer

# --- Command Handlers --- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main menu with embedded buttons."""
    keyboard = [
        [InlineKeyboardButton("🔥 Top Skills This Week", callback_data="top_skills_week")],
        [InlineKeyboardButton("📊 Top Skills This Month", callback_data="top_skills_month")],
        [InlineKeyboardButton("💰 Top Paying Skills", callback_data="top_paying_skills")],
        [InlineKeyboardButton("🔍 Skill Info", callback_data="skill_info")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Welcome to SkillPulse Bot!\n\n"
        "I provide insights about tech job market trends.\n"
        "Use the buttons below to explore analytics.\n\n"
        "Reference: Job data collected from public Telegram job channels.",
        reply_markup=reply_markup
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button clicks."""
    query = update.callback_query
    await query.answer()
    cmd = query.data

    if cmd == "top_skills_week":
        await send_top_skills(update, period="week")
    elif cmd == "top_skills_month":
        await send_top_skills(update, period="month")
    elif cmd == "top_paying_skills":
        await send_top_paying(update)
    elif cmd == "skill_info":
        await show_skill_buttons(update)

# --- Analytics Functions --- #

async def send_top_skills(update: Update, period: str = "week"):
    """Send top skills with chart and reference info."""
    try:
        data_func = top_skills_week if period == "week" else top_skills_month
        data = data_func(limit=10)

        if not data:
            await update.callback_query.message.reply_text("❌ No data available.")
            return

        # Compute date range
        today = datetime.now().date()
        start_date = today - timedelta(days=7 if period == "week" else 30)
        message = f"🔥 Top Skills This {'Week' if period == 'week' else 'Month'}\n"
        message += f"📅 Data from {start_date} to {today}\n"
        message += f"💼 Jobs analyzed: {sum(d['job_count'] for d in data)}\n\n"

        for idx, skill in enumerate(data, 1):
            message += f"{idx}. {skill['skill_name']} — {skill['job_count']} jobs"
            if skill.get("avg_salary"):
                message += f" | Avg Salary: {format_currency(skill['avg_salary'])}"
            message += "\n"

        # Create and send chart
        chart = create_bar_chart(data, f"Top Skills ({'Week' if period=='week' else 'Month'})")
        await update.callback_query.message.reply_photo(photo=chart, caption=message)

    except Exception as e:
        logger.error(f"Error sending top skills ({period}): {e}")
        await update.callback_query.message.reply_text("❌ An error occurred while fetching top skills.")

async def send_top_paying(update: Update):
    """Send top paying skills with chart."""
    try:
        data = top_paying_skills(limit=10)
        if not data:
            await update.callback_query.message.reply_text("❌ No salary data available.")
            return

        today = datetime.now().date()
        message = f"💰 Top Paying Skills\n📅 Data up to {today}\n\n"
        for idx, skill in enumerate(data, 1):
            message += f"{idx}. {skill['skill_name']} — {format_currency(skill['avg_salary'])} | ({skill['job_count']} jobs)\n"

        chart = create_bar_chart(data, "Top Paying Skills", value_key="avg_salary")
        await update.callback_query.message.reply_photo(photo=chart, caption=message)

    except Exception as e:
        logger.error(f"Error sending top paying skills: {e}")
        await update.callback_query.message.reply_text("❌ An error occurred while fetching top paying skills.")

# --- Skill Info Buttons --- #

async def show_skill_buttons(update: Update):
    """Show a list of all skills as buttons for selection."""
    try:
        skills = get_all_skills()
        if not skills:
            await update.callback_query.message.reply_text("❌ No skills found in the database.")
            return

        keyboard = []
        # Split buttons into rows of 2-3 skills for neatness
        row = []
        for idx, skill in enumerate(skills, 1):
            row.append(InlineKeyboardButton(skill, callback_data=f"skill_{skill}"))
            if idx % 3 == 0:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text(
            "🔍 Select a skill to view details:",
            reply_markup=reply_markup
        )

    except Exception as e:
        logger.error(f"Error showing skill buttons: {e}")
        await update.callback_query.message.reply_text("❌ Could not load skill list.")

async def handle_skill_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle a selected skill from the buttons."""
    query = update.callback_query
    await query.answer()
    skill_name = query.data.replace("skill_", "")
    try:
        info = get_skill_info(skill_name)
        if not info:
            await query.message.reply_text(f"❌ Skill '{skill_name}' not found.")
            return
        message = f"📈 {info['skill_name']}\n"
        message += f"💼 Total Jobs: {info['total_jobs']}\n"
        message += f"📅 Jobs (Last 7 days): {info['jobs_last_7_days']}\n"
        message += f"📅 Jobs (Last 30 days): {info['jobs_last_30_days']}\n"
        message += f"💰 Avg Salary: {format_currency(info['avg_salary']) if info['avg_salary'] else 'No data'}\n"
        message += "Reference: Job data collected from public Telegram channels"
        await query.message.reply_text(message)
    except Exception as e:
        logger.error(f"Error fetching skill info: {e}")
        await query.message.reply_text("❌ An error occurred while fetching skill info.")

# --- Main Bot Setup --- #

def create_bot_application() -> Application:
    if not BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN must be set in .env")
    app = Application.builder().token(BOT_TOKEN).build()
    # Commands
    app.add_handler(CommandHandler("start", start))
    # Button clicks
    app.add_handler(CallbackQueryHandler(handle_button, pattern="^(top_skills_week|top_skills_month|top_paying_skills|skill_info)$"))
    app.add_handler(CallbackQueryHandler(handle_skill_button, pattern="^skill_"))
    return app

def run_bot():
    app = create_bot_application()
    logger.info("🚀 SkillPulse bot with buttons, charts, and skill selection is running...")
    app.run_polling(allowed_updates=None)

if __name__ == "__main__":
    run_bot()
