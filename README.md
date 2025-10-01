# Stock Market Information Assistant

A Prefect-powered workflow that provides real-time stock market information through Telegram. This bot listens to Telegram messages, extracts stock queries using AI, fetches data from Yahoo Finance, and responds with formatted stock information.

## Features

- 🤖 **Telegram Integration**: Interact with the bot through Telegram
- 📊 **Real-time Stock Data**: Fetch live stock prices and statistics from Yahoo Finance
- 🧠 **AI-Powered**: Uses OpenAI GPT-4 to understand natural language queries
- 🔄 **Prefect Orchestration**: Reliable workflow execution with retry logic
- 📈 **Comprehensive Data**: Current price, change %, volume, market cap, 52-week range, and more

## How It Works

1. User sends a message to the Telegram bot (company name or ticker symbol)
2. OpenAI GPT-4 extracts the ticker symbol from the message
3. Yahoo Finance API fetches the latest stock data
4. Data is formatted into a user-friendly response
5. Response is sent back to the user via Telegram

## Setup

### Prerequisites

- Python 3.9+
- Telegram Bot Token (create via [@BotFather](https://t.me/botfather))
- OpenAI API Key
- Prefect Cloud account (optional, for deployment)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/AutoflowsDotDev/stock-market-assistant.git
cd stock-market-assistant
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
cp .env.example .env
# Edit .env and add your credentials
```

Required environment variables:

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `OPENAI_API_KEY`: Your OpenAI API key

### Running Locally

```bash
python stock_market_assistant.py
```

## Usage

Once the bot is running, send it a message on Telegram:

- `AAPL` - Get info for Apple stock
- `What's the price of Tesla?` - Natural language query
- `Microsoft` - Query by company name
- `/start` - Welcome message
- `/help` - Show help information

## Deployment to Prefect Cloud

### Deployment is GitHub-Based! 🚀

The workflow is deployed directly from the GitHub repository using `prefect.yaml`.

### Step 1: Authenticate with Prefect Cloud

```bash
prefect cloud login
```

### Step 2: Deploy using prefect.yaml

```bash
# Deploy all deployments (pulls from GitHub)
prefect deploy --all
```

The deployment will automatically clone from:
- **Repository**: https://github.com/AutoflowsDotDev/stock-market-assistant
- **Branch**: `master`

### Step 3: Start a worker

```bash
prefect worker start --pool default-work-pool
```

**Note**: Workers will automatically pull the latest code from GitHub on each run!

See `GITHUB_DEPLOYMENT.md` for detailed GitHub deployment documentation.

## Project Structure

```
.
├── stock_market_assistant.py  # Main workflow file
├── prefect.yaml               # Prefect deployment config (GitHub-based)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── QUICK_START.md            # Quick start guide
├── GITHUB_DEPLOYMENT.md      # GitHub deployment guide
├── DEPLOYMENT_GUIDE.md       # Detailed deployment instructions
├── DEPLOYMENT_SUCCESS.md     # Deployment summary
├── CREDENTIALS_GUIDE.md      # How to get credentials
├── run_bot.sh                # Run bot locally
├── run_worker.sh             # Run Prefect worker
├── check_status.sh           # Check system status
├── setup.py                  # Interactive setup wizard
├── test_simple.py            # Simple tests
├── test_workflow.py          # Full workflow tests
└── .gitignore               # Git ignore file
```

## Technologies Used

- **Prefect**: Workflow orchestration and scheduling
- **python-telegram-bot**: Telegram Bot API integration
- **yfinance**: Yahoo Finance data retrieval
- **OpenAI**: Natural language processing for ticker extraction
- **Pipedream Connect SDK**: (Optional) For managed integrations

## Error Handling

The workflow includes:

- Automatic retries for failed API calls
- Graceful error messages to users
- Comprehensive logging for debugging

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Support

For issues or questions, please open an issue on GitHub.
