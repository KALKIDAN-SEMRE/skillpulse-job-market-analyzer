"""
Script to run the Telegram job collector.
Usage: python run_collector.py
"""

from app.collector import run_collector

# ✅ List of PUBLIC Telegram channel usernames (NO @ symbol)
TELEGRAM_CHANNELS = [
    "DagmawiBabiJobs",
    "ethiotechjobs",
    "addisjobs"
]

# Number of messages to fetch per channel
MESSAGES_PER_CHANNEL = 100


if __name__ == "__main__":
    print("===================================")
    print("🚀 SkillPulse Telegram Collector")
    print("===================================\n")

    print(f"Channels to collect from: {TELEGRAM_CHANNELS}")
    print(f"Messages per channel: {MESSAGES_PER_CHANNEL}\n")

    run_collector(
        channels=TELEGRAM_CHANNELS,
        limit=MESSAGES_PER_CHANNEL
    )
