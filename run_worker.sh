#!/bin/bash

# Load environment variables from .env file
export $(cat .env | grep -v '^#' | xargs)

# Start Prefect worker
echo "🤖 Starting Prefect Worker for Stock Market Assistant..."
echo "Worker will process deployments from Prefect Cloud"
echo "Press Ctrl+C to stop"
echo ""

prefect worker start --pool default-work-pool
