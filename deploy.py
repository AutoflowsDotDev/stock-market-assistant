"""
Deployment script for Stock Market Assistant workflow to Prefect Cloud
"""

from prefect import serve
from stock_market_assistant import stock_market_bot_flow

if __name__ == "__main__":
    # Create deployment
    deployment = stock_market_bot_flow.to_deployment(
        name="stock-market-telegram-bot",
        tags=["telegram", "stocks", "finance", "ai"],
        description="Telegram bot that provides real-time stock market information",
        version="1.0.0",
    )
    
    # Serve the deployment
    serve(deployment)
