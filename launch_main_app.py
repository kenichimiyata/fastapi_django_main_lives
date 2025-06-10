#!/usr/bin/env python3
"""
Launch the main FastAPI+Django application with Gradio interfaces
"""

import os
import sys
import django
import uvicorn

# Set environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# Add to Python path
sys.path.append('/workspaces/fastapi_django_main_live')

if __name__ == "__main__":
    print("🚀 Starting FastAPI+Django+Gradio Application")
    print("=" * 50)
    
    # Configure Django
    django.setup()
    print("✓ Django configured")
    
    # Import and run the application
    try:
        print("✓ Starting on http://localhost:7863")
        print("✓ OpenInterpreter will be available in the Gradio interface")
        
        uvicorn.run(
            "mysite.asgi:app", 
            host="0.0.0.0", 
            port=7863,
            reload=False,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        import traceback
        traceback.print_exc()
