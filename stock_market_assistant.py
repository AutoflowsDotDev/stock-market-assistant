"""
Stock Market Information Assistant
A Prefect workflow that receives stock queries via Telegram,
fetches real-time data from Yahoo Finance, and responds to users.
"""

import os
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime

from prefect import flow, task
import yfinance as yf
from openai import OpenAI
from telegram import Update, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


@task(name="Extract Ticker Symbol", retries=2)
def extract_ticker_symbol(message_text: str) -> Optional[str]:
    """
    Use OpenAI to extract the stock ticker symbol from user message.

    Args:
        message_text: The user's message text

    Returns:
        The ticker symbol or None if not found
    """
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = f"""
        Extract the stock ticker symbol from the following message. 
        If the user mentions a company name, provide the corresponding stock ticker.
        If no stock or company is mentioned, return "NONE".
        Only return the ticker symbol, nothing else.
        
        Message: {message_text}
        
        Examples:
        - "What's the price of Apple?" -> AAPL
        - "Tell me about Tesla stock" -> TSLA
        - "How is Microsoft doing?" -> MSFT
        - "GOOGL" -> GOOGL
        - "Hello" -> NONE
        
        Ticker:
        """

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that extracts stock ticker symbols from user messages.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=10,
            temperature=0,
        )

        ticker = response.choices[0].message.content.strip().upper()

        if ticker == "NONE" or not ticker:
            return None

        logger.info(f"Extracted ticker symbol: {ticker}")
        return ticker

    except Exception as e:
        logger.error(f"Error extracting ticker symbol: {e}")
        return None


@task(name="Fetch Stock Data", retries=3)
def fetch_stock_data(ticker: str) -> Optional[Dict[str, Any]]:
    """
    Fetch stock data from Yahoo Finance using yfinance.

    Args:
        ticker: The stock ticker symbol

    Returns:
        Dictionary containing stock information or None if failed
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Get current price and key statistics
        stock_data = {
            "ticker": ticker,
            "company_name": info.get("longName", ticker),
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "previous_close": info.get("previousClose"),
            "open": info.get("open") or info.get("regularMarketOpen"),
            "day_high": info.get("dayHigh") or info.get("regularMarketDayHigh"),
            "day_low": info.get("dayLow") or info.get("regularMarketDayLow"),
            "volume": info.get("volume") or info.get("regularMarketVolume"),
            "market_cap": info.get("marketCap"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
            "currency": info.get("currency", "USD"),
        }

        logger.info(f"Fetched stock data for {ticker}")
        return stock_data

    except Exception as e:
        logger.error(f"Error fetching stock data for {ticker}: {e}")
        return None


@task(name="Format Stock Response")
def format_stock_response(stock_data: Dict[str, Any]) -> str:
    """
    Format stock data into a user-friendly message.

    Args:
        stock_data: Dictionary containing stock information

    Returns:
        Formatted message string
    """
    try:
        current_price = stock_data.get("current_price")
        previous_close = stock_data.get("previous_close")

        # Calculate change
        change = None
        change_percent = None
        if current_price and previous_close:
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100

        # Build the message
        message = f"📊 *{stock_data['company_name']}* ({stock_data['ticker']})\n\n"

        if current_price:
            message += (
                f"💰 Current Price: {stock_data['currency']} {current_price:.2f}\n"
            )

        if change is not None and change_percent is not None:
            emoji = "📈" if change >= 0 else "📉"
            sign = "+" if change >= 0 else ""
            message += (
                f"{emoji} Change: {sign}{change:.2f} ({sign}{change_percent:.2f}%)\n\n"
            )
        else:
            message += "\n"

        if stock_data.get("open"):
            message += f"🔓 Open: {stock_data['currency']} {stock_data['open']:.2f}\n"

        if stock_data.get("day_high") and stock_data.get("day_low"):
            message += f"📊 Day Range: {stock_data['day_low']:.2f} - {stock_data['day_high']:.2f}\n"

        if stock_data.get("volume"):
            volume_formatted = f"{stock_data['volume']:,}"
            message += f"📦 Volume: {volume_formatted}\n"

        if stock_data.get("market_cap"):
            market_cap_b = stock_data["market_cap"] / 1_000_000_000
            message += f"🏢 Market Cap: {stock_data['currency']} {market_cap_b:.2f}B\n"

        if stock_data.get("52_week_high") and stock_data.get("52_week_low"):
            message += f"\n📅 52-Week Range: {stock_data['52_week_low']:.2f} - {stock_data['52_week_high']:.2f}\n"

        message += f"\n_Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_"

        return message

    except Exception as e:
        logger.error(f"Error formatting stock response: {e}")
        return "Sorry, I encountered an error formatting the stock information."


@task(name="Process Stock Query")
def process_stock_query(message_text: str) -> str:
    """
    Process a stock query end-to-end.

    Args:
        message_text: The user's message

    Returns:
        Response message to send back to user
    """
    # Extract ticker symbol
    ticker = extract_ticker_symbol(message_text)

    if not ticker:
        return (
            "I couldn't identify a stock ticker in your message. "
            "Please mention a company name or ticker symbol (e.g., 'AAPL', 'Apple', 'Tesla')."
        )

    # Fetch stock data
    stock_data = fetch_stock_data(ticker)

    if not stock_data:
        return f"Sorry, I couldn't find stock information for '{ticker}'. Please check the ticker symbol and try again."

    # Format response
    response = format_stock_response(stock_data)

    return response


@flow(name="Stock Market Assistant - Telegram Bot", log_prints=True)
def stock_market_bot_flow():
    """
    Main Prefect flow for the Stock Market Assistant Telegram bot.
    This flow runs continuously and handles incoming Telegram messages.
    """

    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command."""
        welcome_message = (
            "👋 Welcome to the Stock Market Information Assistant!\n\n"
            "I can help you get real-time stock market information.\n\n"
            "Just send me a company name or ticker symbol, and I'll fetch the latest data for you.\n\n"
            "Examples:\n"
            "• AAPL\n"
            "• Tesla\n"
            "• What's the price of Microsoft?\n"
            "• How is Amazon doing?\n\n"
            "Type /help for more information."
        )
        await update.message.reply_text(welcome_message)

    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /help command."""
        help_message = (
            "📖 *Help - Stock Market Assistant*\n\n"
            "Send me any of the following:\n"
            "• Stock ticker symbol (e.g., AAPL, TSLA, MSFT)\n"
            "• Company name (e.g., Apple, Tesla, Microsoft)\n"
            "• Question about a stock (e.g., 'What's the price of Google?')\n\n"
            "I'll provide you with:\n"
            "✓ Current price\n"
            "✓ Price change\n"
            "✓ Day range\n"
            "✓ Volume\n"
            "✓ Market cap\n"
            "✓ 52-week range\n\n"
            "Commands:\n"
            "/start - Start the bot\n"
            "/help - Show this help message"
        )
        await update.message.reply_text(help_message, parse_mode="Markdown")

    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming text messages."""
        try:
            user_message = update.message.text
            chat_id = update.message.chat_id

            logger.info(f"Received message from {chat_id}: {user_message}")

            # Send typing action
            await context.bot.send_chat_action(chat_id=chat_id, action="typing")

            # Process the query using Prefect tasks
            response = process_stock_query(user_message)

            # Send response
            await update.message.reply_text(response, parse_mode="Markdown")

        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text(
                "Sorry, I encountered an error processing your request. Please try again."
            )

    async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors."""
        logger.error(f"Update {update} caused error {context.error}")

    # Get Telegram bot token
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not telegram_token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        raise ValueError("TELEGRAM_BOT_TOKEN is required")

    # Create the Application
    application = Application.builder().token(telegram_token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    application.add_error_handler(error_handler)

    logger.info("Starting Stock Market Assistant Telegram Bot...")
    print("🤖 Stock Market Assistant is running...")
    print("Press Ctrl+C to stop")

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    stock_market_bot_flow()
