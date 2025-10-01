# Credentials Guide

This guide will help you obtain all the necessary credentials to run the Stock Market Assistant.

## 1. Telegram Bot Token

### Steps:
1. Open Telegram and search for `@BotFather`
2. Start a chat and send `/newbot`
3. Follow the prompts to name your bot
4. Copy the **Bot Token** provided (format: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

**Documentation**: https://core.telegram.org/bots#botfather

**Environment Variable**: `TELEGRAM_BOT_TOKEN`

---

## 2. OpenAI API Key

### Steps:
1. Go to https://platform.openai.com/
2. Sign in or create an account
3. Navigate to **API Keys** section
4. Click **"Create new secret key"**
5. Copy the key (format: `sk-...`)
6. Make sure you have credits in your account

**Note**: GPT-4 API access is required. You may need to upgrade your account.

**Environment Variable**: `OPENAI_API_KEY`

---

## 3. Prefect Cloud Account (Optional - for deployment)

### Steps:
1. Go to https://app.prefect.cloud/
2. Sign up for a free account
3. Create a workspace
4. Navigate to **API Keys** in your profile
5. Create a new API key
6. Copy the API key
7. Note your API URL (format: `https://api.prefect.cloud/api/accounts/[ACCOUNT_ID]/workspaces/[WORKSPACE_ID]`)

**Environment Variables**: 
- `PREFECT_API_KEY`
- `PREFECT_API_URL`

---

## Quick Setup

Run the interactive setup script:

```bash
python3 setup.py
```

Or manually create a `.env` file:

```bash
cp .env.example .env
nano .env  # or use your preferred editor
```

Then fill in your credentials:

```env
TELEGRAM_BOT_TOKEN=your_token_here
OPENAI_API_KEY=your_key_here
PREFECT_API_KEY=your_prefect_key_here  # Optional
PREFECT_API_URL=your_prefect_url_here  # Optional
```

## Testing Credentials

Test your setup:

```bash
python3 test_simple.py  # Test Yahoo Finance (no credentials needed)
python3 test_workflow.py  # Test full workflow (requires all credentials)
```

## Security Notes

- ⚠️ **Never commit your `.env` file** to Git (it's in `.gitignore`)
- 🔐 Keep your API keys secure and rotate them regularly
- 💰 Monitor your OpenAI usage to avoid unexpected charges
- 🛡️ Use environment variables or secrets managers in production
