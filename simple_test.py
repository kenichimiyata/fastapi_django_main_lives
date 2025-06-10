#!/usr/bin/env python3

# 最小限のテスト
import ast

def validate_code(code_content):
    if not code_content or not code_content.strip():
        return False
    
    cleaned_code = '\n'.join(line for line in code_content.split('\n') if line.strip())
    if not cleaned_code:
        return False
    
    try:
        ast.parse(cleaned_code)
        return True
    except SyntaxError:
        return False
    except Exception:
        return False

# テスト実行
if __name__ == "__main__":
    print("Testing validate_code function...")
    
    # 正常なコード
    result1 = validate_code('print("Hello")')
    print(f"Valid code test: {result1}")
    
    # エラーコード
    result2 = validate_code('print("Hello"')
    print(f"Invalid code test: {result2}")
    
    # 空のコード
    result3 = validate_code('')
    print(f"Empty code test: {result3}")
    
    print("Test completed successfully!")
