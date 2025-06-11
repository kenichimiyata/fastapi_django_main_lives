#!/bin/bash

echo "🔄 FastAPI Django Main Live - Post Start Setup..."

# Ensure Rust is in PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Check if all dependencies are installed
echo "🔍 Checking dependencies..."
python3 -c "
try:
    import gradio
    import fastapi
    import open_interpreter
    import sqlite3
    print('✅ All core dependencies available')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
    print('Run: pip install -r requirements.txt')
"

# Display helpful information
echo ""
echo "🚀 FastAPI Django Main Live is ready!"
echo ""
echo "📱 Available services:"
echo "  • Main App: http://localhost:7860"
echo "  • Test Manager: http://localhost:7861" 
echo "  • Debug Port: 5678"
echo ""
echo "🛠️ Quick commands:"
echo "  • Start main app: python3 app.py"
echo "  • Start debug mode: python3 app_debug_server.py"
echo "  • Test prompt manager: python3 test_prompt_manager.py"
echo ""
