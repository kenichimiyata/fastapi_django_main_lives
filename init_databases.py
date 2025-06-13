#!/usr/bin/env python3
"""
データベース初期化スクリプト
必要なテーブルとサンプルデータを作成します
"""
import sqlite3
import os
from datetime import datetime

def create_databases():
    """必要なデータベースとテーブルを作成"""
    try:
        # 必要なディレクトリを作成
        os.makedirs('controllers/gra_03_programfromdocs', exist_ok=True)
        print('✅ ディレクトリ作成完了')

        # プロンプトデータベースを作成
        print('📋 プロンプトデータベースを作成中...')
        conn = sqlite3.connect('prompts.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # テストデータを挿入
        cursor.execute('''
            INSERT OR IGNORE INTO prompts (id, title, content, category, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (1, '初回テストプロンプト', 'Hello World を表示するシンプルなPythonスクリプトを作成してください。', 'テスト', datetime.now(), datetime.now()))

        conn.commit()
        conn.close()
        print('✅ プロンプトデータベース作成完了')

        # 承認システムデータベースを作成
        print('📋 承認システムデータベースを作成中...')
        conn = sqlite3.connect('controllers/gra_03_programfromdocs/approval_system.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS approvals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt_id INTEGER,
                approval_status TEXT,
                reason TEXT,
                approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()
        print('✅ 承認システムデータベース作成完了')

        print('🎉 全てのデータベースが正常に作成されました!')
        
        # 確認
        if os.path.exists('prompts.db'):
            print('✅ prompts.db 作成確認')
        if os.path.exists('controllers/gra_03_programfromdocs/approval_system.db'):
            print('✅ approval_system.db 作成確認')
            
        return True
        
    except Exception as e:
        print(f'❌ エラーが発生しました: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_databases()
