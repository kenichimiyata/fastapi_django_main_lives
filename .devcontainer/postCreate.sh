#!/bin/bash

echo "🚀 FastAPI Django Main Live - Post Create Setup Starting..."

# Update system packages
sudo apt-get update

# Install Rust (for tiktoken and other dependencies)
echo "📦 Installing Rust..."
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source ~/.cargo/env

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --upgrade pip setuptools wheel

# Install requirements with better error handling
echo "📋 Installing from requirements.txt..."
pip install -r requirements.txt

# Install additional dependencies for debugging
echo "🔧 Installing debug dependencies..."
pip install debugpy python-dotenv

# Set up environment files
echo "⚙️ Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env 2>/dev/null || echo "GROQ_API_KEY=your_key_here
OPENINTERPRETER_PASSWORD=your_password_here" > .env
    echo "📝 .env file created - please update with your API keys"
fi

# Initialize databases
echo "🗄️ Initializing databases..."
python3 -c "
import sqlite3
import os

# Create prompts database
if not os.path.exists('prompts.db'):
    conn = sqlite3.connect('prompts.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print('✅ Prompts database initialized')

# Create chat history database
if not os.path.exists('chat_history.db'):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            type TEXT,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print('✅ Chat history database initialized')
"

# Set proper permissions
chmod +x .devcontainer/*.sh

echo "✅ FastAPI Django Main Live setup completed!"
echo ""
echo "🎯 Next steps:"
echo "1. Update .env file with your API keys"
echo "2. Run: python3 app.py"
echo "3. Access: http://localhost:7860"
echo ""
echo "🐛 For debugging:"
echo "1. Run: python3 app_debug_server.py"
echo "2. Use VS Code 'Remote Attach' configuration"
echo ""
