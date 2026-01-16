#!/bin/bash

# Quick test script for ClickUp integration
# Run this on your local machine with internet access

echo "🧪 ClickUp Integration Test"
echo "============================="
echo ""

# Set your credentials
export CLICKUP_ACCESS_TOKEN='pk_106141823_INXP08ZZWGBDSQHJK9ZZB84IR7MOKUFS'

# Test task ID
TASK_ID='86aeg64f4'

echo "1️⃣  Testing task status fetch..."
./clickup-claude status "$TASK_ID"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Status command works!"
    echo ""
    echo "2️⃣  Testing autonomous execution (simulated)..."
    ./clickup-claude execute "$TASK_ID"
else
    echo ""
    echo "❌ Test failed. Check your access token and task ID."
fi
