#!/usr/bin/env python3
"""
統合プロンプト承認システム - メインアプリ統合版
Simple LauncherとIntegrated Dashboardの機能を統合
"""

import gradio as gr
import sqlite3
import os
import json
import sys
from datetime import datetime
from typing import List, Dict, Optional

# 統一データベースヘルパーをインポート
try:
    from .db_helper import get_unified_db_connection, ensure_unified_tables
except ImportError:
    # パスを追加してconfig/database.pyにアクセス
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..')
    sys.path.append(project_root)
    
    def get_unified_db_connection(db_name='approval_system'):
        try:
            from config.database import get_db_connection
            return get_db_connection(db_name)
        except ImportError:
            db_path = f"/workspaces/fastapi_django_main_lives/database/{db_name}.db"
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            return sqlite3.connect(db_path)
    
    def ensure_unified_tables():
        try:
            from config.database import ensure_tables_exist
            ensure_tables_exist()
        except ImportError:
            pass

def init_integrated_db():
    """統合データベース初期化"""
    try:
        # 統一された設定を使用
        ensure_unified_tables()
        conn = get_unified_db_connection('approval_system')
    except Exception as e:
        print(f"Warning: Failed to use unified database config: {e}")
        # フォールバック: 直接接続
        db_path = "/workspaces/fastapi_django_main_lives/database/approval_system.db"
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 承認キューテーブル
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS approval_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            source TEXT DEFAULT 'manual',
            priority INTEGER DEFAULT 3,
            status TEXT DEFAULT 'pending',
            github_issue_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            approved_at TIMESTAMP,
            approved_by TEXT
        )
    ''')
    
    # 実行ログテーブル（拡張版）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS execution_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            result_url TEXT,
            execution_time REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            details TEXT,
            github_repo_url TEXT,
            folder_name TEXT
        )
    ''')
    
    # システム統計テーブル
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE,
            prompts_added INTEGER DEFAULT 0,
            systems_generated INTEGER DEFAULT 0,
            approvals_processed INTEGER DEFAULT 0,
            github_repos_created INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()

def get_approval_queue() -> List[Dict]:
    """承認キュー取得"""
    conn = get_unified_db_connection('approval_system')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, issue_title, issue_body, requester, priority, approval_status, github_repo, created_at, approved_at
        FROM approval_queue 
        ORDER BY priority ASC, created_at ASC
    ''')
    queue = cursor.fetchall()
    conn.close()
    
    return [
        {
            'id': q[0],
            'title': q[1],
            'content': q[2],
            'source': q[3],
            'priority': q[4],
            'status': q[5],
            'github_issue_url': q[6] or '',
            'created_at': q[7],
            'approved_at': q[8]
        }
        for q in queue
    ]

def add_to_approval_queue(title: str, content: str, source: str = "manual", priority: int = 3) -> str:
    """承認キューに追加"""
    if not title or not content:
        return "❌ タイトルと内容を入力してください"
    
    conn = get_unified_db_connection('approval_system')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO approval_queue (issue_title, issue_body, requester, priority) VALUES (?, ?, ?, ?)',
        (title, content, source, priority)
    )
    conn.commit()
    conn.close()
    
    return f"✅ '{title}' を承認キューに追加しました（優先度: {priority}）"

def approve_request(request_id: int) -> str:
    """リクエスト承認"""
    conn = get_unified_db_connection('approval_system')
    cursor = conn.cursor()
    
    # リクエスト情報取得
    cursor.execute('SELECT issue_title, issue_body FROM approval_queue WHERE id = ?', (request_id,))
    request = cursor.fetchone()
    
    if not request:
        conn.close()
        return "❌ リクエストが見つかりません"
    
    title, content = request
    
    # ステータス更新
    cursor.execute(
        'UPDATE approval_queue SET approval_status = ?, approved_at = ? WHERE id = ?',
        ('approved', datetime.now().isoformat(), request_id)
    )
    
    # プロンプトテーブルに追加
    cursor.execute('''
        INSERT INTO prompts (title, content, execution_status, created_at)
        VALUES (?, ?, ?, ?)
    ''', (f"承認済み: {title}", content, "approved", datetime.now().isoformat()))
    
    # 実行ログに記録
    cursor.execute(
        'INSERT INTO execution_log (title, status, details) VALUES (?, ?, ?)',
        (title, 'approved', f'承認されたプロンプト: {content[:100]}...')
    )
    
    conn.commit()
    conn.close()
    
    return f"✅ '{title}' を承認し、プロンプトシステムに追加しました"

def reject_request(request_id: int, reason: str = "") -> str:
    """リクエスト拒否"""
    conn = get_unified_db_connection('approval_system')
    cursor = conn.cursor()
    
    # リクエスト情報取得
    cursor.execute('SELECT issue_title FROM approval_queue WHERE id = ?', (request_id,))
    request = cursor.fetchone()
    
    if not request:
        conn.close()
        return "❌ リクエストが見つかりません"
    
    title = request[0]
    
    cursor.execute(
        'UPDATE approval_queue SET approval_status = ? WHERE id = ?',
        ('rejected', request_id)
    )
    
    # 実行ログに記録
    cursor.execute(
        'INSERT INTO execution_log (title, status, details) VALUES (?, ?, ?)',
        (title, 'rejected', f'拒否理由: {reason or "未指定"}')
    )
    
    conn.commit()
    conn.close()
    
    return f"❌ '{title}' を拒否しました。理由: {reason or '未指定'}"

def get_execution_logs() -> List[Dict]:
    """実行ログ取得"""
    conn = get_unified_db_connection('approval_system')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, approval_id, status, github_repo_url, execution_start, execution_end, result_summary, error_message
        FROM execution_log 
        ORDER BY execution_start DESC 
        LIMIT 50
    ''')
    logs = cursor.fetchall()
    conn.close()
    
    return [
        {
            'id': l[0],
            'title': f'実行ログID: {l[0]} (承認ID: {l[1]})',
            'status': l[2] or 'unknown',
            'result_url': l[3] or '',
            'execution_time': 0 if not l[4] or not l[5] else (
                (datetime.fromisoformat(l[5]) - datetime.fromisoformat(l[4])).total_seconds()
            ),
            'created_at': l[4] or 'Unknown',
            'details': l[6] or '',
            'github_repo_url': l[3] or ''
        }
        for l in logs
    ]

def get_system_status() -> Dict:
    """システム状況取得"""
    try:
        # プロンプト統計（prompts.dbから）
        prompts_conn = get_unified_db_connection('prompts')
        prompts_cursor = prompts_conn.cursor()
        prompts_cursor.execute('SELECT COUNT(*) FROM prompts')
        total_prompts = prompts_cursor.fetchone()[0]
        
        # 今日のプロンプト
        today = datetime.now().strftime('%Y-%m-%d')
        prompts_cursor.execute('SELECT COUNT(*) FROM prompts WHERE DATE(created_at) = ?', (today,))
        today_prompts = prompts_cursor.fetchone()[0]
        prompts_conn.close()
        
        # 承認システム統計（approval_system.dbから）
        approval_conn = get_unified_db_connection('approval_system')
        approval_cursor = approval_conn.cursor()
        
        approval_cursor.execute('SELECT COUNT(*) FROM approval_queue WHERE approval_status = "pending_review"')
        pending_approvals = approval_cursor.fetchone()[0]
        
        approval_cursor.execute('SELECT COUNT(*) FROM approval_queue WHERE DATE(created_at) = ?', (today,))
        today_requests = approval_cursor.fetchone()[0]
        
        # execution_logテーブルがある場合のみ実行
        try:
            approval_cursor.execute('SELECT COUNT(*) FROM execution_log WHERE status = "completed"')
            completed_executions = approval_cursor.fetchone()[0]
        except:
            completed_executions = 0
            
        approval_conn.close()
        
    except Exception as e:
        # エラーが発生した場合はデフォルト値を返す
        print(f"Warning: Database error in get_system_status: {e}")
        total_prompts = 0
        pending_approvals = 0
        completed_executions = 0
        today_prompts = 0
        today_requests = 0
    
    return {
        'total_prompts': total_prompts,
        'pending_approvals': pending_approvals,
        'completed_executions': completed_executions,
        'today_prompts': today_prompts,
        'today_requests': today_requests
    }

def create_gradio_interface():
    """統合承認システムGradioインターフェース"""
    
    init_integrated_db()
    
    with gr.Blocks(title="🎯 統合承認システム", theme="soft") as interface:
        gr.Markdown("""
        # 🎯 統合プロンプト承認システム
        
        **GitHub ISSUE → 承認ワークフロー → システム生成**の統合管理
        """)
        
        with gr.Tabs():
            # システム状況タブ
            with gr.TabItem("📊 システム状況"):
                with gr.Row():
                    with gr.Column():
                        status_display = gr.Markdown("📈 システム状況を読み込み中...")
                        refresh_status_btn = gr.Button("🔄 状況更新", variant="secondary")
                    
                    with gr.Column():
                        gr.Markdown("""
                        ### 💡 システム概要
                        - **承認システム**: プロンプト実行の承認ワークフロー
                        - **GitHub連携**: ISSUE → プロンプト → 自動生成
                        - **統合管理**: 複数システムの一元管理
                        """)
                
                def update_status():
                    stats = get_system_status()
                    return f"""
## 📊 システム統計

### 📋 基本統計
- **総プロンプト数**: {stats['total_prompts']}件
- **承認待ち**: {stats['pending_approvals']}件  
- **実行完了**: {stats['completed_executions']}件

### 📅 今日の活動
- **新規プロンプト**: {stats['today_prompts']}件
- **承認リクエスト**: {stats['today_requests']}件

### 🔗 統合状況
- **GitHub ISSUE自動化**: ✅ 統合済み
- **プロンプト管理**: ✅ 統合済み
- **自動実行システム**: ✅ 統合済み
                    """
                
                refresh_status_btn.click(update_status, outputs=[status_display])
                interface.load(update_status, outputs=[status_display])
            
            # 承認キュー管理タブ
            with gr.TabItem("✅ 承認管理"):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### 📤 新規承認リクエスト")
                        req_title = gr.Textbox(label="タイトル", placeholder="システム生成リクエストのタイトル")
                        req_content = gr.Textbox(
                            label="内容", 
                            lines=8,
                            placeholder="生成したいシステムの詳細要件を記述..."
                        )
                        req_priority = gr.Slider(
                            label="優先度", 
                            minimum=1, 
                            maximum=5, 
                            value=3, 
                            step=1,
                            info="1=最高優先度, 5=最低優先度"
                        )
                        submit_btn = gr.Button("📨 承認リクエスト送信", variant="primary")
                        submit_result = gr.Textbox(label="送信結果", interactive=False)
                    
                    with gr.Column():
                        gr.Markdown("### ⏳ 承認待ちキュー")
                        approval_queue = gr.Dataframe(
                            headers=["ID", "タイトル", "ソース", "優先度", "ステータス", "作成日時"],
                            interactive=False
                        )
                        refresh_queue_btn = gr.Button("🔄 キュー更新")
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### 🎯 承認アクション")
                        action_id = gr.Number(label="対象ID", precision=0, info="承認/拒否するリクエストのID")
                        
                        with gr.Row():
                            approve_btn = gr.Button("✅ 承認", variant="primary")
                            reject_btn = gr.Button("❌ 拒否", variant="stop")
                        
                        reject_reason = gr.Textbox(label="拒否理由（任意）", lines=2)
                        action_result = gr.Textbox(label="アクション結果", interactive=False)
                
                def refresh_queue():
                    queue = get_approval_queue()
                    return [[
                        q['id'], 
                        q['title'][:50] + ('...' if len(q['title']) > 50 else ''),
                        q['source'], 
                        q['priority'], 
                        q['status'],
                        q['created_at'][:16]
                    ] for q in queue if q['status'] == 'pending_review']
                
                def submit_request_wrapper(title, content, priority):
                    result = add_to_approval_queue(title, content, "manual", int(priority))
                    return result, "", "", 3, refresh_queue()
                
                submit_btn.click(
                    submit_request_wrapper,
                    inputs=[req_title, req_content, req_priority],
                    outputs=[submit_result, req_title, req_content, req_priority, approval_queue]
                )
                
                approve_btn.click(
                    lambda id_val: approve_request(int(id_val)) if id_val else "❌ IDを入力してください",
                    inputs=[action_id],
                    outputs=[action_result]
                ).then(refresh_queue, outputs=[approval_queue])
                
                reject_btn.click(
                    lambda id_val, reason: reject_request(int(id_val), reason) if id_val else "❌ IDを入力してください",
                    inputs=[action_id, reject_reason],
                    outputs=[action_result]
                ).then(refresh_queue, outputs=[approval_queue])
                
                refresh_queue_btn.click(refresh_queue, outputs=[approval_queue])
                interface.load(refresh_queue, outputs=[approval_queue])
            
            # 実行ログタブ
            with gr.TabItem("📈 実行ログ"):
                gr.Markdown("### 📊 システム実行履歴")
                
                execution_logs = gr.Dataframe(
                    headers=["ID", "タイトル", "ステータス", "実行時間", "作成日時", "GitHub"],
                    interactive=False
                )
                refresh_logs_btn = gr.Button("🔄 ログ更新")
                
                def refresh_logs():
                    logs = get_execution_logs()
                    return [[
                        l['id'], 
                        l['title'][:40] + ('...' if len(l['title']) > 40 else ''),
                        l['status'], 
                        f"{l['execution_time']:.1f}s" if l['execution_time'] else "N/A",
                        l['created_at'][:16],
                        "🔗" if l['github_repo_url'] else ""
                    ] for l in logs]
                
                refresh_logs_btn.click(refresh_logs, outputs=[execution_logs])
                interface.load(refresh_logs, outputs=[execution_logs])
            
            # システム設定タブ
            with gr.TabItem("⚙️ 設定"):
                gr.Markdown("""
                ## 🔧 統合承認システム設定
                
                ### 📋 システム構成
                - **データベース**: `/workspaces/fastapi_django_main_live/prompts.db`
                - **統合ポート**: 7860（メインアプリ）
                - **GitHub連携**: 環境変数 `GITHUB_TOKEN`
                
                ### 🚀 統合済み機能
                1. **Simple Launcher**: プロンプト承認ワークフロー
                2. **Integrated Dashboard**: GitHub ISSUE監視
                3. **UI Fix Verification**: システム検証
                
                ### 📊 承認ワークフロー
                1. **リクエスト作成** → 承認キューに追加
                2. **承認/拒否** → 管理者による審査
                3. **自動実行** → 承認済みプロンプトの実行
                4. **結果通知** → GitHub/Google Chat通知
                
                ### 🔗 外部連携
                - **GitHub ISSUE**: 自動プロンプト抽出
                - **GPT-ENGINEER**: システム自動生成
                - **Google Chat**: 進捗通知
                """)
        
        return interface

# インターフェースタイトル（自動検出用）
interface_title = "🎯 統合承認システム"

# メインアプリ用のインターフェースオブジェクト
gradio_interface = create_gradio_interface()

if __name__ == "__main__":
    gradio_interface.launch(share=False, server_name="0.0.0.0", server_port=7865)
