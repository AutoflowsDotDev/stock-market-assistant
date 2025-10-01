"""
Interactive setup script for Stock Market Assistant
"""

import os
import sys

def setup_environment():
    """Interactive setup for environment variables."""
    print("🚀 Stock Market Assistant - Setup Wizard")
    print("=" * 60)
    print()
    
    # Check if .env already exists
    env_file = ".env"
    if os.path.exists(env_file):
        response = input("⚠️  .env file already exists. Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("Setup cancelled.")
            return
    
    print("Please provide the following credentials:")
    print()
    
    # Telegram Bot Token
    print("1. Telegram Bot Token")
    print("   Create a bot via @BotFather on Telegram: https://t.me/botfather")
    telegram_token = input("   Enter your Telegram Bot Token: ").strip()
    
    # OpenAI API Key
    print("\n2. OpenAI API Key")
    print("   Get your API key from: https://platform.openai.com/api-keys")
    openai_key = input("   Enter your OpenAI API Key: ").strip()
    
    # Optional: Prefect Cloud
    print("\n3. Prefect Cloud (Optional - for deployment)")
    prefect_key = input("   Enter your Prefect API Key (or press Enter to skip): ").strip()
    prefect_url = ""
    if prefect_key:
        prefect_url = input("   Enter your Prefect API URL: ").strip()
    
    # Write to .env file
    with open(env_file, 'w') as f:
        f.write("# Telegram Bot Configuration\n")
        f.write(f"TELEGRAM_BOT_TOKEN={telegram_token}\n\n")
        
        f.write("# OpenAI API Configuration\n")
        f.write(f"OPENAI_API_KEY={openai_key}\n\n")
        
        if prefect_key:
            f.write("# Prefect Cloud Configuration\n")
            f.write(f"PREFECT_API_KEY={prefect_key}\n")
            f.write(f"PREFECT_API_URL={prefect_url}\n")
    
    print("\n✅ Configuration saved to .env file")
    print("\n📝 Next steps:")
    print("   1. Test the workflow: python test_workflow.py")
    print("   2. Run the bot: python stock_market_assistant.py")
    print("   3. Deploy to Prefect Cloud: python deploy.py")
    print()


if __name__ == "__main__":
    setup_environment()
