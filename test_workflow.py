"""
Test script for Stock Market Assistant workflow components
"""

import os
from dotenv import load_dotenv
from stock_market_assistant import extract_ticker_symbol, fetch_stock_data, format_stock_response

# Load environment variables
load_dotenv()

def test_ticker_extraction():
    """Test the ticker symbol extraction functionality."""
    print("\n🧪 Testing Ticker Extraction...")
    
    test_messages = [
        "What's the price of Apple?",
        "TSLA",
        "Tell me about Microsoft",
        "How is Amazon doing?",
        "GOOGL stock price"
    ]
    
    for message in test_messages:
        print(f"\nMessage: '{message}'")
        ticker = extract_ticker_symbol(message)
        print(f"Extracted Ticker: {ticker}")


def test_stock_data_fetch():
    """Test fetching stock data from Yahoo Finance."""
    print("\n\n📊 Testing Stock Data Fetch...")
    
    test_tickers = ["AAPL", "TSLA", "MSFT"]
    
    for ticker in test_tickers:
        print(f"\nFetching data for {ticker}...")
        stock_data = fetch_stock_data(ticker)
        
        if stock_data:
            print(f"✓ Successfully fetched data for {stock_data['company_name']}")
            print(f"  Current Price: {stock_data.get('current_price')}")
        else:
            print(f"✗ Failed to fetch data for {ticker}")


def test_response_formatting():
    """Test the response formatting."""
    print("\n\n💬 Testing Response Formatting...")
    
    # Fetch real data for Apple
    stock_data = fetch_stock_data("AAPL")
    
    if stock_data:
        response = format_stock_response(stock_data)
        print("\nFormatted Response:")
        print("=" * 50)
        print(response)
        print("=" * 50)
    else:
        print("✗ Could not test formatting - failed to fetch stock data")


def main():
    """Run all tests."""
    print("🚀 Starting Stock Market Assistant Tests")
    print("=" * 60)
    
    # Check environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set. Ticker extraction will fail.")
    
    if not os.getenv("TELEGRAM_BOT_TOKEN"):
        print("⚠️  Warning: TELEGRAM_BOT_TOKEN not set. Bot cannot run.")
    
    # Run tests
    test_stock_data_fetch()
    
    if os.getenv("OPENAI_API_KEY"):
        test_ticker_extraction()
        test_response_formatting()
    else:
        print("\n⏭️  Skipping AI-related tests (no OpenAI API key)")
    
    print("\n\n✅ Tests completed!")


if __name__ == "__main__":
    main()
