#!/usr/bin/env python3
"""
OpenInterpreter の基本機能テスト
"""

import sys
import os

# パスを追加
sys.path.append('/workspaces/fastapi_django_main_live')

def test_basic_imports():
    """基本的なインポートテスト"""
    print("=== 基本インポートテスト ===")
    
    try:
        import gradio as gr
        print("✓ Gradio imported successfully")
    except Exception as e:
        print(f"❌ Gradio import failed: {e}")
    
    try:
        from controllers.gra_02_openInterpreter.OpenInterpreter import validate_code
        print("✓ validate_code imported successfully")
        
        # テスト実行
        result = validate_code('print("Hello, World!")')
        print(f"✓ validate_code test result: {result}")
        
        result2 = validate_code('print("Hello, World!"')  # 構文エラー
        print(f"✓ validate_code error test result: {result2}")
        
    except Exception as e:
        print(f"❌ validate_code import failed: {e}")
        import traceback
        traceback.print_exc()

def test_interpreter_import():
    """interpreter のインポートテスト"""
    print("\n=== Interpreter インポートテスト ===")
    
    try:
        from interpreter import interpreter
        print("✓ open-interpreter imported successfully")
        print(f"✓ interpreter object: {type(interpreter)}")
    except Exception as e:
        print(f"❌ open-interpreter import failed: {e}")

def test_env_variables():
    """環境変数テスト"""
    print("\n=== 環境変数テスト ===")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    groq_key = os.getenv("GROQ_API_KEY")
    api_key = os.getenv("api_key")
    
    print(f"GROQ_API_KEY set: {bool(groq_key)}")
    print(f"api_key set: {bool(api_key)}")
    
    if groq_key:
        print(f"GROQ_API_KEY format: {groq_key[:10]}...")

def test_chat_function():
    """チャット関数の基本テスト"""
    print("\n=== チャット関数テスト ===")
    
    try:
        from controllers.gra_02_openInterpreter.OpenInterpreter import chat_with_interpreter
        print("✓ chat_with_interpreter imported successfully")
        
        # 簡単なテスト（パスワードエラーを期待）
        responses = list(chat_with_interpreter("Hello", passw="wrong"))
        print(f"✓ Password error test: {len(responses)} responses")
        if responses:
            print(f"   First response: {responses[0][:100]}")
        
    except Exception as e:
        print(f"❌ chat_with_interpreter test failed: {e}")
        import traceback
        traceback.print_exc()

def test_database():
    """データベーステスト"""
    print("\n=== データベーステスト ===")
    
    try:
        from controllers.gra_02_openInterpreter.OpenInterpreter import (
            initialize_db, 
            add_message_to_db, 
            get_recent_messages
        )
        
        print("✓ Database functions imported successfully")
        
        # データベース初期化
        initialize_db()
        print("✓ Database initialized")
        
        # テストメッセージ追加
        add_message_to_db("user", "message", "Test message")
        print("✓ Test message added")
        
        # メッセージ取得
        messages = get_recent_messages(limit=3)
        print(f"✓ Retrieved {len(messages)} messages")
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 OpenInterpreter 診断テスト開始")
    print("=" * 50)
    
    test_basic_imports()
    test_interpreter_import()
    test_env_variables()
    test_database()
    test_chat_function()
    
    print("\n" + "=" * 50)
    print("🏁 診断テスト完了")
