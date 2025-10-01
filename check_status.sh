#!/bin/bash

echo "🔍 Stock Market Assistant - Status Check"
echo "========================================"
echo ""

# Check if bot is running
if pgrep -f "stock_market_assistant.py" > /dev/null; then
    echo "✅ Bot Status: RUNNING"
    echo "   Process ID: $(pgrep -f stock_market_assistant.py)"
else
    echo "❌ Bot Status: NOT RUNNING"
    echo "   Start with: ./run_bot.sh"
fi
echo ""

# Check environment variables
if [ -f .env ]; then
    echo "✅ .env file: EXISTS"
else
    echo "❌ .env file: NOT FOUND"
    echo "   Run: python3 setup.py"
fi
echo ""

# Check Prefect connection
echo "🔗 Prefect Cloud Status:"
prefect profile ls 2>/dev/null | grep -q "cloud-profile"
if [ $? -eq 0 ]; then
    echo "✅ Prefect Profile: CONFIGURED"
    echo "   Profile: cloud-profile"
else
    echo "❌ Prefect Profile: NOT CONFIGURED"
fi
echo ""

# Check dependencies
echo "📦 Dependencies:"
python3 -c "import telegram, yfinance, openai, prefect; print('✅ All packages installed')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Some packages missing"
    echo "   Run: pip install -r requirements.txt"
fi
echo ""

# Get bot info if running
if pgrep -f "stock_market_assistant.py" > /dev/null; then
    echo "📊 Resource Usage:"
    ps aux | grep stock_market_assistant.py | grep -v grep | awk '{print "   CPU: "$3"% | Memory: "$4"%"}'
fi
echo ""

echo "🔗 Quick Links:"
echo "   GitHub: https://github.com/AutoflowsDotDev/stock-market-assistant"
echo "   Prefect: https://app.prefect.cloud/"
echo ""

echo "💡 Commands:"
echo "   Start bot: ./run_bot.sh"
echo "   Stop bot:  pkill -f stock_market_assistant.py"
echo "   View logs: tail -f nohup.out"
echo ""
