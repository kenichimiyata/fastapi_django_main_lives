"""
会話履歴管理システム
=====================

GitHub Copilotとの会話履歴をSQLiteに保存し、
Gradioインターフェースで閲覧・検索できるシステム

機能:
- 会話の自動保存
- 履歴の閲覧・検索
- 会話の分析・統計
- エクスポート機能
"""

import gradio as gr
import sqlite3
import json
import datetime
from typing import List, Dict, Optional, Tuple
import os
import pandas as pd
from pathlib import Path
import re

# インターフェースメタデータ
interface_title = "💬 会話履歴管理"
interface_description = "GitHub Copilotとの会話履歴を管理・閲覧"

class ConversationManager:
    def __init__(self, db_path: str = "conversation_history.db"):
        """会話履歴管理クラスの初期化"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """データベースの初期化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 会話テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_message TEXT NOT NULL,
                assistant_response TEXT NOT NULL,
                context_info TEXT,
                files_involved TEXT,
                tools_used TEXT,
                conversation_summary TEXT,
                tags TEXT,
                project_name TEXT DEFAULT 'ContBK統合システム',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # セッションテーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                session_name TEXT,
                start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                end_time DATETIME,
                total_messages INTEGER DEFAULT 0,
                description TEXT,
                project_context TEXT
            )
        ''')
        
        # インデックス作成
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON conversations(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_session_id ON conversations(session_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tags ON conversations(tags)')
        
        conn.commit()
        conn.close()
        print("✅ 会話履歴データベース初期化完了")
    
    def save_conversation(self, 
                         session_id: str,
                         user_message: str, 
                         assistant_response: str,
                         context_info: str = "",
                         files_involved: str = "",
                         tools_used: str = "",
                         tags: str = ""):
        """会話を保存"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 会話を保存
        cursor.execute('''
            INSERT INTO conversations 
            (session_id, user_message, assistant_response, context_info, 
             files_involved, tools_used, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, user_message, assistant_response, context_info,
              files_involved, tools_used, tags))
        
        # セッション更新
        cursor.execute('''
            INSERT OR REPLACE INTO sessions 
            (session_id, session_name, total_messages)
            VALUES (?, ?, (
                SELECT COUNT(*) FROM conversations 
                WHERE session_id = ?
            ))
        ''', (session_id, f"セッション_{session_id[:8]}", session_id))
        
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    def get_conversations(self, 
                         limit: int = 50, 
                         session_id: str = None,
                         search_query: str = None) -> List[Dict]:
        """会話履歴を取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT id, session_id, timestamp, user_message, 
                   assistant_response, context_info, files_involved, 
                   tools_used, tags
            FROM conversations
            WHERE 1=1
        '''
        params = []
        
        if session_id:
            query += " AND session_id = ?"
            params.append(session_id)
        
        if search_query:
            query += " AND (user_message LIKE ? OR assistant_response LIKE ?)"
            params.extend([f"%{search_query}%", f"%{search_query}%"])
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        conversations = []
        for row in rows:
            conversations.append({
                'id': row[0],
                'session_id': row[1],
                'timestamp': row[2],
                'user_message': row[3],
                'assistant_response': row[4],
                'context_info': row[5],
                'files_involved': row[6],
                'tools_used': row[7],
                'tags': row[8]
            })
        
        return conversations
    
    def get_sessions(self) -> List[Dict]:
        """セッション一覧を取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT session_id, session_name, start_time, 
                   total_messages, description
            FROM sessions
            ORDER BY start_time DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        sessions = []
        for row in rows:
            sessions.append({
                'session_id': row[0],
                'session_name': row[1],
                'start_time': row[2],
                'total_messages': row[3],
                'description': row[4]
            })
        
        return sessions
    
    def get_statistics(self) -> Dict:
        """統計情報を取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 基本統計
        cursor.execute('SELECT COUNT(*) FROM conversations')
        total_conversations = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT session_id) FROM sessions')
        total_sessions = cursor.fetchone()[0]
        
        # 今日の会話数
        cursor.execute('''
            SELECT COUNT(*) FROM conversations 
            WHERE DATE(timestamp) = DATE('now')
        ''')
        today_conversations = cursor.fetchone()[0]
        
        # 最も使用されたツール
        cursor.execute('''
            SELECT tools_used, COUNT(*) as count
            FROM conversations 
            WHERE tools_used != ''
            GROUP BY tools_used
            ORDER BY count DESC
            LIMIT 5
        ''')
        top_tools = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_conversations': total_conversations,
            'total_sessions': total_sessions,
            'today_conversations': today_conversations,
            'top_tools': top_tools
        }

# グローバルインスタンス
conversation_manager = ConversationManager()

# ConversationManagerクラスもエクスポート
__all__ = ['ConversationManager', 'conversation_manager']

def format_conversation_display(conversations: List[Dict]) -> str:
    """会話履歴を表示用にフォーマット"""
    if not conversations:
        return "📭 会話履歴がありません"
    
    display_text = "# 📚 会話履歴\n\n"
    
    for conv in conversations:
        timestamp = conv['timestamp']
        user_msg = conv['user_message'][:100] + "..." if len(conv['user_message']) > 100 else conv['user_message']
        assistant_resp = conv['assistant_response'][:200] + "..." if len(conv['assistant_response']) > 200 else conv['assistant_response']
        
        display_text += f"""
## 🕐 {timestamp}
**👤 ユーザー:** {user_msg}

**🤖 アシスタント:** {assistant_resp}

**📁 関連ファイル:** {conv.get('files_involved', 'なし')}
**🔧 使用ツール:** {conv.get('tools_used', 'なし')}
**🏷️ タグ:** {conv.get('tags', 'なし')}

---
"""
    
    return display_text

def load_conversation_history(limit: int, session_filter: str, search_query: str) -> Tuple[str, str]:
    """会話履歴をロード"""
    try:
        # フィルター処理
        session_id = session_filter if session_filter != "全てのセッション" else None
        search = search_query.strip() if search_query.strip() else None
        
        conversations = conversation_manager.get_conversations(
            limit=limit,
            session_id=session_id,
            search_query=search
        )
        
        display_text = format_conversation_display(conversations)
        
        # 統計情報
        stats = conversation_manager.get_statistics()
        stats_text = f"""
## 📊 統計情報
- **総会話数:** {stats['total_conversations']}
- **総セッション数:** {stats['total_sessions']}
- **今日の会話数:** {stats['today_conversations']}
"""
        
        return display_text, stats_text
        
    except Exception as e:
        return f"❌ エラーが発生しました: {str(e)}", ""

def get_session_list() -> List[str]:
    """セッション一覧を取得"""
    try:
        sessions = conversation_manager.get_sessions()
        session_list = ["全てのセッション"]
        session_list.extend([f"{s['session_name']} ({s['session_id'][:8]})" for s in sessions])
        return session_list
    except:
        return ["全てのセッション"]

def save_sample_conversation():
    """サンプル会話を保存（テスト用）"""
    import uuid
    session_id = str(uuid.uuid4())
    
    conversation_manager.save_conversation(
        session_id=session_id,
        user_message="ContBK統合システムについて教えて",
        assistant_response="ContBK統合システムは、contbkフォルダーにある全てのGradioインターフェースを美しい絵文字タイトル付きで統合表示するシステムです。",
        context_info="ContBK統合システムの説明",
        files_involved="controllers/contbk_example.py",
        tools_used="create_file, insert_edit_into_file",
        tags="contbk, gradio, 統合システム"
    )
    
    return "✅ サンプル会話を保存しました"

def export_conversations_csv(conversations: List[Dict]) -> str:
    """会話履歴をCSVエクスポート"""
    try:
        if not conversations:
            return "📭 エクスポートする会話がありません"
        
        df = pd.DataFrame(conversations)
        
        # CSVファイルとして保存
        export_path = f"conversation_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(export_path, index=False, encoding='utf-8-sig')
        
        return f"✅ 会話履歴をエクスポートしました: {export_path}"
    except Exception as e:
        return f"❌ エクスポートエラー: {str(e)}"

# Gradioインターフェース作成
def create_conversation_interface():
    """会話履歴管理インターフェースを作成"""
    
    with gr.Blocks(title="💬 会話履歴管理", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 💬 会話履歴管理システム")
        gr.Markdown("GitHub Copilotとの会話履歴を管理・閲覧できます")
        
        with gr.Tab("📚 履歴閲覧"):
            with gr.Row():
                with gr.Column(scale=2):
                    search_box = gr.Textbox(
                        label="🔍 検索", 
                        placeholder="キーワードで検索...",
                        value=""
                    )
                with gr.Column(scale=2):
                    session_dropdown = gr.Dropdown(
                        label="📋 セッション選択",
                        choices=get_session_list(),
                        value="全てのセッション"
                    )
                with gr.Column(scale=1):
                    limit_slider = gr.Slider(
                        label="📊 表示件数",
                        minimum=10,
                        maximum=100,
                        value=20,
                        step=10
                    )
            
            with gr.Row():
                load_btn = gr.Button("🔄 履歴読み込み", variant="primary")
                refresh_btn = gr.Button("🆕 セッション更新")
                export_btn = gr.Button("📥 CSV エクスポート")
            
            with gr.Row():
                with gr.Column(scale=3):
                    conversation_display = gr.Markdown(
                        value="🔄 履歴読み込みボタンを押してください"
                    )
                with gr.Column(scale=1):
                    stats_display = gr.Markdown(
                        value="📊 統計情報"
                    )
        
        with gr.Tab("💾 会話保存"):
            gr.Markdown("## ✍️ 新しい会話を手動保存")
            
            with gr.Row():
                session_id_input = gr.Textbox(
                    label="🆔 セッションID",
                    placeholder="自動生成または手動入力",
                    value=""
                )
                tags_input = gr.Textbox(
                    label="🏷️ タグ",
                    placeholder="カンマ区切りでタグを入力",
                    value=""
                )
            
            user_message_input = gr.Textbox(
                label="👤 ユーザーメッセージ",
                lines=3,
                placeholder="ユーザーからのメッセージ..."
            )
            
            assistant_response_input = gr.Textbox(
                label="🤖 アシスタント応答",
                lines=5,
                placeholder="アシスタントの応答..."
            )
            
            with gr.Row():
                files_input = gr.Textbox(
                    label="📁 関連ファイル",
                    placeholder="関連ファイルパス",
                    value=""
                )
                tools_input = gr.Textbox(
                    label="🔧 使用ツール",
                    placeholder="使用したツール名",
                    value=""
                )
            
            save_btn = gr.Button("💾 会話を保存", variant="primary")
            sample_btn = gr.Button("📝 サンプル保存", variant="secondary")
            
            save_result = gr.Textbox(label="💬 結果", interactive=False)
        
        with gr.Tab("📊 統計・分析"):
            gr.Markdown("## 📈 会話統計ダッシュボード")
            
            with gr.Row():
                refresh_stats_btn = gr.Button("🔄 統計更新", variant="primary")
            
            detailed_stats = gr.Markdown(
                value="🔄 統計更新ボタンを押してください"
            )
        
        # イベントハンドラー
        load_btn.click(
            fn=load_conversation_history,
            inputs=[limit_slider, session_dropdown, search_box],
            outputs=[conversation_display, stats_display]
        )
        
        refresh_btn.click(
            fn=lambda: gr.Dropdown.update(choices=get_session_list()),
            outputs=[session_dropdown]
        )
        
        sample_btn.click(
            fn=save_sample_conversation,
            outputs=[save_result]
        )
        
        # 初期ロード
        interface.load(
            fn=load_conversation_history,
            inputs=[gr.Number(value=20), gr.Textbox(value="全てのセッション"), gr.Textbox(value="")],
            outputs=[conversation_display, stats_display]
        )
    
    return interface

# Gradioインターフェースのインスタンス作成
gradio_interface = create_conversation_interface()

if __name__ == "__main__":
    print("🚀 会話履歴管理システム起動中...")
    gradio_interface.launch(
        server_port=7870,
        share=False,
        debug=True
    )
