#!/bin/bash

# Set script to exit immediately if a command fails
set -e

# Display ASCII art banner
echo "======================================================"
echo "  ___ ___ ___ _    _____ ___ ___ _  _ "
echo " / __| _ \_ _| |  |_   _| __/ __| || |"
echo " \__ \  _/| || |__  | | | _| (__| __ |"
echo " |___/_| |___|____| |_| |___\___|_||_|"
echo ""
echo " Test Automation Framework Demo"
echo "======================================================"

# Check if running in CI environment
if [ -n "$CI" ]; then
  echo "Running in CI environment"
  HEADLESS="--headless"
else
  HEADLESS=""
fi

# Set up Python environment
echo "Setting up environment..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python -m venv venv
fi

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
  source venv/Scripts/activate
fi

# Install requirements
echo "Installing requirements..."
pip install -q -r automation_framework/requirements.txt

# Make sure Python can find the automation_framework package
echo "Setting up PYTHONPATH..."
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Make sure the reports directory exists
mkdir -p reports

# Default browser is Chrome
BROWSER=${1:-chrome}
echo "Using browser: $BROWSER"

# Run tests with desired configuration
echo "Running web tests from The Internet example app..."
python -m pytest examples/web_the_internet/tests/ \
  --browser=$BROWSER \
  $HEADLESS \
  -v

echo "======================================================"
echo "Test execution completed!"
echo "Reports available in the reports/ directory"
echo "======================================================"

# Deactivate virtual environment
deactivate