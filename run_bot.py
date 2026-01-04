"""
Script to run the SkillPulse Telegram bot.
Usage: python run_bot.py
"""
from bot import run_bot

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 SkillPulse Telegram Bot")
    print("=" * 50)
    print("\nStarting bot...")
    print("Press Ctrl+C to stop\n")
    
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\n\nBot stopped by user.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("\nMake sure TELEGRAM_BOT_TOKEN is set in your .env file")
        print("Get your bot token from @BotFather on Telegram")

