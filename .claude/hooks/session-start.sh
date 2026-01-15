#!/bin/bash
set -euo pipefail

# Only run in Claude Code on the web (remote environments)
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

echo "Setting up development environment..."

# Node.js / JavaScript / TypeScript
if [ -f "package.json" ]; then
  echo "Installing Node.js dependencies..."
  if [ -f "package-lock.json" ]; then
    npm install
  elif [ -f "yarn.lock" ]; then
    yarn install
  elif [ -f "pnpm-lock.yaml" ]; then
    pnpm install
  else
    npm install
  fi
fi

# Python
if [ -f "requirements.txt" ]; then
  echo "Installing Python dependencies from requirements.txt..."
  pip install -r requirements.txt
elif [ -f "pyproject.toml" ]; then
  echo "Installing Python dependencies from pyproject.toml..."
  if command -v poetry &> /dev/null; then
    poetry install
  else
    pip install -e .
  fi
fi

# Ruby
if [ -f "Gemfile" ]; then
  echo "Installing Ruby gems..."
  bundle install
fi

# Go
if [ -f "go.mod" ]; then
  echo "Installing Go dependencies..."
  go mod download
fi

# Rust
if [ -f "Cargo.toml" ]; then
  echo "Building Rust project..."
  cargo build
fi

echo "Development environment setup complete!"
