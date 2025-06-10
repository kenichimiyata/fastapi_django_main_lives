#!/usr/bin/env python3
"""
Test the main Gradio interfaces setup
"""

import os
import sys
import django
from django.conf import settings

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# Add the project directory to Python path
sys.path.append('/workspaces/fastapi_django_main_live')

# Configure Django
django.setup()

def test_gradio_setup():
    print("Testing Gradio interface setup...")
    
    try:
        from mysite.routers.gradio import setup_gradio_interfaces
        print("✓ Successfully imported setup_gradio_interfaces")
        
        # Create the interfaces
        tabs = setup_gradio_interfaces()
        print("✓ Successfully created Gradio tabs")
        
        # Check if tabs were created
        if tabs:
            print(f"✓ Created tabs interface with components")
            # TabbedInterface doesn't have tab_names directly accessible, but we can check the type
            print(f"✓ Interface type: {type(tabs).__name__}")
            if hasattr(tabs, 'fns') and tabs.fns:
                print(f"✓ Number of interfaces: {len(tabs.fns)}")
        else:
            print("❌ No tabs created")
            
        return tabs
        
    except Exception as e:
        print(f"❌ Error setting up Gradio interfaces: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_openinterpreter_specific():
    print("\nTesting OpenInterpreter specific import...")
    
    try:
        from controllers.gra_02_openInterpreter.OpenInterpreter import gradio_interface, chat_with_interpreter
        print("✓ Successfully imported OpenInterpreter components")
        print(f"✓ Gradio interface type: {type(gradio_interface)}")
        print(f"✓ Chat function available: {callable(chat_with_interpreter)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error importing OpenInterpreter: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing Main Application Gradio Setup")
    print("=" * 50)
    
    # Test basic setup
    tabs = test_gradio_setup()
    
    # Test specific OpenInterpreter
    oi_success = test_openinterpreter_specific()
    
    if tabs and oi_success:
        print("\n✅ All tests passed! The Gradio system should be working.")
        print("🚀 You can now start the main application.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
