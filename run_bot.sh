#!/bin/bash

# Load environment variables from .env file
export $(cat .env | grep -v '^#' | xargs)

# Run the Stock Market Assistant bot
echo "🚀 Starting Stock Market Assistant Telegram Bot..."
echo "Press Ctrl+C to stop"
echo ""

python3 stock_market_assistant.py
