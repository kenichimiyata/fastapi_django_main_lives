#!/usr/bin/env python3
"""
OpenInterpreter 直接テスト
"""

import sys
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

# パスを追加
sys.path.append('/workspaces/fastapi_django_main_live')

def test_chat_function():
    """chat_with_interpreter関数を直接テスト"""
    try:
        from controllers.gra_02_openInterpreter.OpenInterpreter import chat_with_interpreter
        
        print("🧪 Testing chat_with_interpreter function")
        print("=" * 50)
        
        # テストメッセージ
        test_messages = [
            "Hello, can you help me?",
            "What is Django?",
            "How do I create a PostgreSQL table?",
            "Show me a simple Python function"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n📝 Test {i}: {message}")
            print("-" * 30)
            
            try:
                responses = []
                for response in chat_with_interpreter(message, passw="12345"):
                    responses.append(str(response))
                    print(f"Response chunk {len(responses)}: {str(response)[:100]}...")
                    
                    # 最大5つの応答で制限
                    if len(responses) >= 5:
                        break
                
                print(f"✅ Test {i} completed. Got {len(responses)} response chunks.")
                
                if responses:
                    final_response = responses[-1]
                    print(f"Final response length: {len(final_response)} characters")
                    if len(final_response) > 200:
                        print(f"Response preview: {final_response[:200]}...")
                    else:
                        print(f"Full response: {final_response}")
                else:
                    print("❌ No responses received")
                
            except Exception as e:
                print(f"❌ Test {i} failed: {e}")
            
            print() # 空行
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Test error: {e}")

def test_environment():
    """環境設定をテスト"""
    print("🔍 Environment Test")
    print("=" * 30)
    
    # API キー
    groq_key = os.getenv("GROQ_API_KEY")
    api_key = os.getenv("api_key")
    print(f"GROQ_API_KEY: {'✅ Set' if groq_key else '❌ Not set'}")
    print(f"api_key: {'✅ Set' if api_key else '❌ Not set'}")
    
    if groq_key:
        print(f"GROQ_API_KEY format: {'✅ Valid' if groq_key.startswith('gsk_') else '❌ Invalid'}")
    
    # データベース
    db_url = os.getenv("postgre_url")
    print(f"postgre_url: {'✅ Set' if db_url else '❌ Not set'}")
    
    # インタープリター
    try:
        from interpreter import interpreter
        print("open-interpreter: ✅ Available")
    except ImportError:
        print("open-interpreter: ❌ Not available")

def test_code_validation():
    """コード検証機能をテスト"""
    print("🔍 Code Validation Test")
    print("=" * 30)
    
    try:
        from controllers.gra_02_openInterpreter.OpenInterpreter import validate_code
        
        test_codes = [
            ("print('Hello, World!')", True),
            ("x = 5\ny = 10\nprint(x + y)", True),
            ("print('unclosed string", False),
            ("if True", False),
            ("", False),
            ("   \n\n  ", False),
            ("# Just a comment", False),
        ]
        
        for code, expected in test_codes:
            result = validate_code(code)
            status = "✅" if result == expected else "❌"
            print(f"{status} Code: {repr(code[:30])} -> Expected: {expected}, Got: {result}")
        
    except ImportError as e:
        print(f"❌ Cannot import validate_code: {e}")

if __name__ == "__main__":
    print("🚀 OpenInterpreter Direct Test")
    print("=" * 50)
    
    test_environment()
    print()
    test_code_validation()
    print()
    test_chat_function()
    
    print("\n🎯 Test completed!")
