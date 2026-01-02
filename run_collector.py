"""
Script to run the Telegram job collector.
Usage: python run_collector.py
"""
from app.collector import run_collector

# List of Telegram channel usernames to collect from (without @)
# Add your channels here
TELEGRAM_CHANNELS = [
    # Example channels (replace with actual job channels):
    # "it_jobs_ru",  # Russian IT jobs channel example
    # "python_jobs",  # Python jobs channel example
    # Add more channels as needed
]

# Number of messages to fetch per channel
MESSAGES_PER_CHANNEL = 100


if __name__ == "__main__":
    if not TELEGRAM_CHANNELS:
        print("ERROR: No Telegram channels specified!")
        print("Please edit run_collector.py and add channel usernames to TELEGRAM_CHANNELS list.")
        print("\nExample:")
        print('  TELEGRAM_CHANNELS = ["channel1", "channel2"]')
        exit(1)
    
    print(f"Starting collection from {len(TELEGRAM_CHANNELS)} channel(s)...")
    print(f"Fetching up to {MESSAGES_PER_CHANNEL} messages per channel\n")
    
    run_collector(TELEGRAM_CHANNELS, MESSAGES_PER_CHANNEL)

