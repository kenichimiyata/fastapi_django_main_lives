#!/usr/bin/env python3
"""
データベース接続テスト用スクリプト
Django+PostgreSQLの接続をテストします
"""

import os
import sys
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

def test_postgresql_connection():
    """PostgreSQL接続をテスト"""
    try:
        import psycopg2
        
        # 環境変数から接続情報を取得
        db_url = os.getenv("postgre_url")
        if not db_url:
            print("❌ postgre_url environment variable not found")
            return False
        
        print(f"🔗 Testing PostgreSQL connection...")
        print(f"Database URL: {db_url[:50]}...")
        
        # データベースに接続
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        # 簡単なクエリを実行
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ PostgreSQL connection successful!")
        print(f"Database version: {version[0][:100]}...")
        
        # テーブル一覧を取得
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"📊 Found {len(tables)} tables in the database:")
        for table in tables[:5]:  # 最初の5つのテーブルを表示
            print(f"  - {table[0]}")
        if len(tables) > 5:
            print(f"  ... and {len(tables) - 5} more tables")
        
        cursor.close()
        conn.close()
        return True
        
    except ImportError:
        print("❌ psycopg2 not installed. Install with: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def test_sqlite_connection():
    """SQLite接続をテスト"""
    try:
        import sqlite3
        
        db_path = "/workspaces/fastapi_django_main_live/chat_history.db"
        print(f"🔗 Testing SQLite connection...")
        print(f"Database path: {db_path}")
        
        if not os.path.exists(db_path):
            print("❌ SQLite database file not found")
            return False
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # テーブル一覧を取得
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"✅ SQLite connection successful!")
        print(f"📊 Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # history テーブルのレコード数を確認
        cursor.execute("SELECT COUNT(*) FROM history;")
        count = cursor.fetchone()[0]
        print(f"💬 Chat history records: {count}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ SQLite connection failed: {e}")
        return False

def test_django_settings():
    """Django設定をテスト"""
    try:
        sys.path.append('/workspaces/fastapi_django_main_live')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
        
        import django
        django.setup()
        
        from django.conf import settings
        from django.db import connection
        
        print(f"🔗 Testing Django database connection...")
        
        # データベース接続をテスト
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        
        print(f"✅ Django database connection successful!")
        print(f"Database engine: {settings.DATABASES['default']['ENGINE']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Django database connection failed: {e}")
        return False

def create_test_table():
    """テスト用テーブルを作成"""
    try:
        import psycopg2
        
        db_url = os.getenv("postgre_url")
        if not db_url:
            print("❌ Cannot create test table: no database URL")
            return False
        
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        # items テーブルを作成
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            brand_name VARCHAR(255),
            model_name VARCHAR(255),
            product_number VARCHAR(255),
            purchase_store VARCHAR(255),
            purchase_date DATE,
            purchase_price INTEGER,
            accessories TEXT,
            condition INTEGER,
            metal_type VARCHAR(255),
            metal_weight DECIMAL(10, 2),
            diamond_certification BYTEA,
            initial BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        print(f"🏗️ Creating items table...")
        cursor.execute(create_table_sql)
        
        # サンプルデータを挿入
        insert_sql = """
        INSERT INTO items (brand_name, model_name, product_number, purchase_store, 
                          purchase_date, purchase_price, metal_type, metal_weight, initial)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
        """
        
        sample_data = [
            ("Rolex", "Submariner", "126610LN", "正規店", "2023-01-15", 1200000, "ステンレス", 150.50, True),
            ("Cartier", "Tank", "WSTA0018", "並行輸入", "2023-02-20", 800000, "ゴールド", 45.20, True),
            ("Omega", "Speedmaster", "311.30.42.30.01.005", "中古店", "2023-03-10", 450000, "ステンレス", 155.00, False)
        ]
        
        cursor.executemany(insert_sql, sample_data)
        
        conn.commit()
        print(f"✅ items table created and sample data inserted!")
        
        # 作成されたデータを確認
        cursor.execute("SELECT COUNT(*) FROM items;")
        count = cursor.fetchone()[0]
        print(f"📊 Total items in table: {count}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to create test table: {e}")
        return False

def main():
    """メイン関数"""
    print("🧪 Database Connection Test Suite")
    print("=" * 40)
    
    tests = [
        ("PostgreSQL Connection", test_postgresql_connection),
        ("SQLite Connection", test_sqlite_connection),
        ("Django Settings", test_django_settings),
        ("Create Test Table", create_test_table)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        print("-" * 30)
        success = test_func()
        results.append((test_name, success))
    
    print(f"\n📊 Test Results Summary")
    print("=" * 40)
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Database connections are working.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
