"""
Simple test without Prefect to verify core functionality
"""

import yfinance as yf
from datetime import datetime


def test_yahoo_finance():
    """Test Yahoo Finance data fetching."""
    print("📊 Testing Yahoo Finance Integration")
    print("=" * 60)

    tickers = ["AAPL", "TSLA", "MSFT"]

    for ticker in tickers:
        try:
            print(f"\n🔍 Fetching data for {ticker}...")
            stock = yf.Ticker(ticker)
            info = stock.info

            company_name = info.get("longName", ticker)
            current_price = info.get("currentPrice") or info.get("regularMarketPrice")
            previous_close = info.get("previousClose")
            market_cap = info.get("marketCap")

            print(f"✓ {company_name}")
            print(
                f"  Current Price: ${current_price:.2f}"
                if current_price
                else "  Price: N/A"
            )
            if previous_close:
                change = current_price - previous_close if current_price else 0
                change_pct = (change / previous_close) * 100 if previous_close else 0
                print(f"  Change: ${change:.2f} ({change_pct:+.2f}%)")
            if market_cap:
                print(f"  Market Cap: ${market_cap/1e9:.2f}B")

        except Exception as e:
            print(f"✗ Error fetching {ticker}: {e}")


if __name__ == "__main__":
    test_yahoo_finance()
    print("\n✅ Test completed!")
