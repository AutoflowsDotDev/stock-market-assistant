# Deployment Guide to Prefect Cloud

This guide will walk you through deploying the Stock Market Assistant to Prefect Cloud.

## Prerequisites

1. ✅ Python 3.9+ installed
2. ✅ Git repository created (Done!)
3. ✅ Credentials obtained (see CREDENTIALS_GUIDE.md)
4. 🔲 Prefect Cloud account
5. 🔲 Environment variables configured

---

## Step 1: Set Up Environment Variables

Create a `.env` file with your credentials:

```bash
cp .env.template .env
```

Or run the interactive setup:

```bash
python3 setup.py
```

Required variables:
- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token
- `OPENAI_API_KEY` - Your OpenAI API key
- `PREFECT_API_KEY` - Your Prefect Cloud API key
- `PREFECT_API_URL` - Your Prefect Cloud API URL

---

## Step 2: Test Locally

Before deploying, test the workflow locally:

### Test Yahoo Finance integration (no credentials needed):
```bash
python3 test_simple.py
```

### Test with your credentials:
```bash
# Load environment variables
source .env  # or export $(cat .env | xargs)

# Run the bot locally
python3 stock_market_assistant.py
```

Test the bot by sending messages on Telegram!

---

## Step 3: Login to Prefect Cloud

```bash
prefect cloud login
```

When prompted:
1. Choose your workspace
2. Or paste your API key directly

Verify connection:
```bash
prefect profile ls
```

---

## Step 4: Create a Work Pool

```bash
prefect work-pool create default-agent-pool --type process
```

---

## Step 5: Deploy the Workflow

### Option A: Using the deployment script
```bash
python3 deploy.py
```

### Option B: Using Prefect CLI
```bash
prefect deploy stock_market_assistant.py:stock_market_bot_flow \
  --name stock-market-telegram-bot \
  --pool default-agent-pool \
  --tag telegram \
  --tag stocks \
  --tag finance
```

---

## Step 6: Configure Secrets in Prefect Cloud

For production, store sensitive credentials in Prefect Cloud:

1. Go to https://app.prefect.cloud/
2. Navigate to **Blocks** → **Add Block**
3. Create a **Secret** block for each credential:
   - `telegram-bot-token`
   - `openai-api-key`

Update the workflow to use Prefect Secrets instead of environment variables.

---

## Step 7: Start a Worker

### Option A: Local worker (for testing)
```bash
prefect worker start --pool default-agent-pool
```

### Option B: Cloud worker (recommended for production)
Deploy to a cloud server (AWS, GCP, Azure, etc.) and run:
```bash
prefect worker start --pool default-agent-pool
```

Keep the worker running (use systemd, supervisor, or Docker).

---

## Step 8: Run the Deployment

### Trigger manually from CLI:
```bash
prefect deployment run stock-market-assistant/stock-market-telegram-bot
```

### Or from Prefect Cloud UI:
1. Go to **Deployments**
2. Find `stock-market-telegram-bot`
3. Click **Quick Run**

---

## Production Deployment Options

### Docker Deployment

Create a Dockerfile:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["prefect", "worker", "start", "--pool", "default-agent-pool"]
```

Build and run:
```bash
docker build -t stock-market-assistant .
docker run -d --env-file .env stock-market-assistant
```

### Kubernetes Deployment

Use Prefect's Kubernetes work pool for scalable deployments.

### Cloud Run / Lambda

Deploy the worker as a serverless function for cost-effective hosting.

---

## Monitoring

- **Prefect Cloud Dashboard**: Monitor flow runs, logs, and errors
- **Telegram**: Test by sending messages to your bot
- **Logs**: Check Prefect logs for debugging

---

## Troubleshooting

### Bot not responding:
- Check that the worker is running
- Verify environment variables are set
- Check Prefect Cloud logs

### API errors:
- Verify API keys are correct
- Check API rate limits
- Ensure OpenAI account has credits

### Connection issues:
- Check internet connectivity
- Verify Prefect API URL is correct
- Ensure firewall allows outbound connections

---

## Next Steps

- Add more features (alerts, portfolio tracking, etc.)
- Implement database for user preferences
- Add support for multiple languages
- Create scheduled reports
- Integrate with more data sources

---

## Support

- GitHub Issues: https://github.com/AutoflowsDotDev/stock-market-assistant/issues
- Prefect Docs: https://docs.prefect.io/
- Telegram Bot API: https://core.telegram.org/bots/api
