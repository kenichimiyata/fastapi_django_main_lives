"""
RPAシステム with Gradio
========================

Playwright + Gradio を使った Web RPA システム

機能:
- 🎯 ウェブページスクリーンショット
- 🖱️ 画面操作自動化
- 📸 画像比較・認識
- 🔄 定期実行・監視
- 📊 実行履歴・ログ管理
"""

import asyncio
import os
import sys
import datetime
import json
import sqlite3
from typing import Optional, List, Dict, Tuple
from pathlib import Path
import traceback

import gradio as gr
from PIL import Image, ImageDraw, ImageChops
import io
import base64

# Playwrightのインポート（遅延インポート）
try:
    from playwright.async_api import async_playwright, Browser, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️ Playwright not installed. Install with: pip install playwright && playwright install")

# インターフェースメタデータ
interface_title = "🤖 RPA自動化システム"
interface_description = "Playwright + Gradio による Web RPA・画面自動化"

class RPAManager:
    def __init__(self, db_path: str = "rpa_history.db"):
        """RPA管理システムの初期化"""
        self.db_path = db_path
        self.init_database()
        self.browser = None
        self.page = None
        
    def init_database(self):
        """データベース初期化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # RPA実行履歴テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rpa_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                url TEXT,
                action_type TEXT NOT NULL,
                parameters TEXT,
                screenshot_path TEXT,
                success BOOLEAN,
                error_message TEXT,
                execution_time REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # RPAタスクテンプレートテーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rpa_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_name TEXT NOT NULL UNIQUE,
                description TEXT,
                actions TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ RPA データベース初期化完了")
    
    async def capture_screenshot(self, url: str, selector: str = None, wait_time: int = 3) -> Tuple[Image.Image, str]:
        """
        ウェブページのスクリーンショットを取得
        
        Args:
            url: 対象URL
            selector: 特定要素のセレクタ（オプション）
            wait_time: 待機時間（秒）
            
        Returns:
            (画像, エラーメッセージ)
        """
        if not PLAYWRIGHT_AVAILABLE:
            return None, "Playwright がインストールされていません"
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # ページ読み込み
                await page.goto(url, wait_until='networkidle')
                
                # 待機
                await asyncio.sleep(wait_time)
                
                # スクリーンショット取得
                if selector:
                    # 特定要素のスクリーンショット
                    element = await page.query_selector(selector)
                    if element:
                        screenshot_bytes = await element.screenshot()
                    else:
                        screenshot_bytes = await page.screenshot()
                        return None, f"セレクタ '{selector}' が見つかりません"
                else:
                    # ページ全体のスクリーンショット
                    screenshot_bytes = await page.screenshot(full_page=True)
                
                await browser.close()
                
                # PIL画像に変換
                img = Image.open(io.BytesIO(screenshot_bytes))
                
                # 実行履歴を保存
                self.save_execution(
                    task_name="スクリーンショット取得",
                    url=url,
                    action_type="screenshot",
                    parameters=json.dumps({"selector": selector, "wait_time": wait_time}),
                    success=True
                )
                
                return img, "✅ スクリーンショット取得成功"
                
        except Exception as e:
            error_msg = f"❌ エラー: {str(e)}"
            
            # エラーログを保存
            self.save_execution(
                task_name="スクリーンショット取得",
                url=url,
                action_type="screenshot",
                parameters=json.dumps({"selector": selector, "wait_time": wait_time}),
                success=False,
                error_message=str(e)
            )
            
            return None, error_msg
    
    async def click_element(self, url: str, selector: str, wait_time: int = 3) -> Tuple[Image.Image, str]:
        """
        要素をクリックして結果をキャプチャ
        
        Args:
            url: 対象URL
            selector: クリック対象のセレクタ
            wait_time: クリック後の待機時間
            
        Returns:
            (クリック後の画像, メッセージ)
        """
        if not PLAYWRIGHT_AVAILABLE:
            return None, "Playwright がインストールされていません"
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # ページ読み込み
                await page.goto(url, wait_until='networkidle')
                
                # 要素を待機してクリック
                await page.wait_for_selector(selector, timeout=10000)
                await page.click(selector)
                
                # 待機
                await asyncio.sleep(wait_time)
                
                # クリック後のスクリーンショット
                screenshot_bytes = await page.screenshot(full_page=True)
                await browser.close()
                
                img = Image.open(io.BytesIO(screenshot_bytes))
                
                # 実行履歴を保存
                self.save_execution(
                    task_name="要素クリック",
                    url=url,
                    action_type="click",
                    parameters=json.dumps({"selector": selector, "wait_time": wait_time}),
                    success=True
                )
                
                return img, f"✅ 要素クリック成功: {selector}"
                
        except Exception as e:
            error_msg = f"❌ クリックエラー: {str(e)}"
            
            self.save_execution(
                task_name="要素クリック",
                url=url,
                action_type="click",
                parameters=json.dumps({"selector": selector, "wait_time": wait_time}),
                success=False,
                error_message=str(e)
            )
            
            return None, error_msg
    
    async def fill_form(self, url: str, form_data: Dict[str, str], submit_selector: str = None) -> Tuple[Image.Image, str]:
        """
        フォーム入力と送信
        
        Args:
            url: 対象URL
            form_data: {セレクタ: 入力値} の辞書
            submit_selector: 送信ボタンのセレクタ
            
        Returns:
            (実行後の画像, メッセージ)
        """
        if not PLAYWRIGHT_AVAILABLE:
            return None, "Playwright がインストールされていません"
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                await page.goto(url, wait_until='networkidle')
                
                # フォーム入力
                for selector, value in form_data.items():
                    await page.wait_for_selector(selector, timeout=10000)
                    await page.fill(selector, value)
                    await asyncio.sleep(0.5)
                
                # 送信ボタンクリック
                if submit_selector:
                    await page.click(submit_selector)
                    await asyncio.sleep(3)
                
                # 結果のスクリーンショット
                screenshot_bytes = await page.screenshot(full_page=True)
                await browser.close()
                
                img = Image.open(io.BytesIO(screenshot_bytes))
                
                self.save_execution(
                    task_name="フォーム入力",
                    url=url,
                    action_type="fill_form",
                    parameters=json.dumps({"form_data": form_data, "submit_selector": submit_selector}),
                    success=True
                )
                
                return img, "✅ フォーム入力・送信成功"
                
        except Exception as e:
            error_msg = f"❌ フォーム入力エラー: {str(e)}"
            
            self.save_execution(
                task_name="フォーム入力",
                url=url,
                action_type="fill_form",
                parameters=json.dumps({"form_data": form_data, "submit_selector": submit_selector}),
                success=False,
                error_message=str(e)
            )
            
            return None, error_msg
    
    def save_execution(self, task_name: str, url: str, action_type: str, 
                      parameters: str, success: bool, error_message: str = None):
        """実行履歴をデータベースに保存"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO rpa_executions 
                (task_name, url, action_type, parameters, success, error_message)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (task_name, url, action_type, parameters, success, error_message))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ 実行履歴保存エラー: {e}")
    
    def get_execution_history(self, limit: int = 20) -> List[Dict]:
        """実行履歴を取得"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT task_name, url, action_type, success, error_message, created_at
                FROM rpa_executions 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    "task_name": row[0],
                    "url": row[1],
                    "action_type": row[2],
                    "success": row[3],
                    "error_message": row[4],
                    "created_at": row[5]
                }
                for row in rows
            ]
        except Exception as e:
            print(f"⚠️ 履歴取得エラー: {e}")
            return []

# グローバルインスタンス
rpa_manager = RPAManager()

def create_rpa_interface():
    """RPA Gradio インターフェースを作成"""
    
    def screenshot_wrapper(url, selector, wait_time):
        """スクリーンショット取得のラッパー関数"""
        if not url:
            return None, "❌ URLを入力してください"
        
        try:
            img, message = asyncio.run(rpa_manager.capture_screenshot(url, selector or None, wait_time))
            return img, message
        except Exception as e:
            return None, f"❌ エラー: {str(e)}"
    
    def click_wrapper(url, selector, wait_time):
        """クリック操作のラッパー関数"""
        if not url or not selector:
            return None, "❌ URLとセレクタを入力してください"
        
        try:
            img, message = asyncio.run(rpa_manager.click_element(url, selector, wait_time))
            return img, message
        except Exception as e:
            return None, f"❌ エラー: {str(e)}"
    
    def get_history_display():
        """実行履歴を表示用フォーマットで取得"""
        history = rpa_manager.get_execution_history(10)
        if not history:
            return "📊 実行履歴はありません"
        
        lines = ["# 🕒 RPA実行履歴", ""]
        for i, record in enumerate(history, 1):
            status = "✅" if record["success"] else "❌"
            lines.append(f"## {i}. {status} {record['task_name']}")
            lines.append(f"- **URL**: {record['url']}")
            lines.append(f"- **アクション**: {record['action_type']}")
            lines.append(f"- **日時**: {record['created_at']}")
            if record["error_message"]:
                lines.append(f"- **エラー**: {record['error_message']}")
            lines.append("")
        
        return "\n".join(lines)
    
    with gr.Blocks(title="🤖 RPA自動化システム", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🤖 RPA自動化システム")
        gr.Markdown("Playwright + Gradio による Web自動化・画面操作ツール")
        
        if not PLAYWRIGHT_AVAILABLE:
            gr.Markdown("""
            ## ⚠️ セットアップが必要です
            
            Playwrightをインストールしてください:
            ```bash
            pip install playwright
            playwright install
            ```
            """)
        
        with gr.Tab("📸 スクリーンショット"):
            gr.Markdown("## 🎯 ウェブページキャプチャ")
            
            with gr.Row():
                with gr.Column(scale=2):
                    url_input = gr.Textbox(
                        label="🌐 URL",
                        placeholder="https://example.com",
                        value="https://www.google.com"
                    )
                with gr.Column(scale=1):
                    wait_time = gr.Slider(
                        label="⏱️ 待機時間(秒)",
                        minimum=1,
                        maximum=10,
                        value=3,
                        step=1
                    )
            
            selector_input = gr.Textbox(
                label="🎯 セレクタ (オプション)",
                placeholder="body, .class-name, #id-name など",
                value=""
            )
            
            screenshot_btn = gr.Button("📸 スクリーンショット取得", variant="primary", size="lg")
            
            with gr.Row():
                screenshot_output = gr.Image(label="📷 取得画像")
                screenshot_message = gr.Textbox(label="📝 実行結果", lines=3)
            
            screenshot_btn.click(
                screenshot_wrapper,
                inputs=[url_input, selector_input, wait_time],
                outputs=[screenshot_output, screenshot_message]
            )
        
        with gr.Tab("🖱️ 画面操作"):
            gr.Markdown("## 🎯 要素クリック・操作")
            
            with gr.Row():
                click_url = gr.Textbox(
                    label="🌐 URL",
                    placeholder="https://example.com",
                    scale=2
                )
                click_wait = gr.Slider(
                    label="⏱️ 待機時間",
                    minimum=1,
                    maximum=10,
                    value=3,
                    scale=1
                )
            
            click_selector = gr.Textbox(
                label="🎯 クリック対象セレクタ",
                placeholder="button, .btn, #submit など",
                value=""
            )
            
            click_btn = gr.Button("🖱️ クリック実行", variant="primary", size="lg")
            
            with gr.Row():
                click_output = gr.Image(label="📷 実行後画像")
                click_message = gr.Textbox(label="📝 実行結果", lines=3)
            
            click_btn.click(
                click_wrapper,
                inputs=[click_url, click_selector, click_wait],
                outputs=[click_output, click_message]
            )
        
        with gr.Tab("📊 実行履歴"):
            gr.Markdown("## 🕒 RPA実行履歴")
            
            refresh_btn = gr.Button("🔄 履歴更新", variant="secondary")
            history_display = gr.Markdown(value=get_history_display())
            
            refresh_btn.click(
                get_history_display,
                outputs=history_display
            )
        
        with gr.Tab("ℹ️ ヘルプ"):
            gr.Markdown("""
            ## 📚 RPA自動化システム ヘルプ
            
            ### 🎯 機能概要
            - **📸 スクリーンショット**: ウェブページの画面キャプチャ
            - **🖱️ 画面操作**: 要素のクリック、フォーム入力
            - **📊 履歴管理**: 実行履歴の記録・表示
            
            ### 🔧 セレクタ例
            - **要素タイプ**: `button`, `input`, `a`
            - **クラス**: `.btn`, `.form-control`, `.nav-link`
            - **ID**: `#submit`, `#login-form`, `#search-box`
            - **属性**: `[name="email"]`, `[type="submit"]`
            
            ### 💡 使用例
            1. **Google検索**: 
               - URL: `https://www.google.com`
               - セレクタ: `[name="q"]` (検索ボックス)
            
            2. **ボタンクリック**:
               - セレクタ: `button`, `.btn-primary`, `#submit-btn`
            
            ### ⚠️ 注意事項
            - 対象サイトの利用規約を確認してください
            - 過度なアクセスは避けてください
            - エラーが発生した場合は履歴を確認してください
            """)
    
    return interface

# このファイルのメインエクスポート
gradio_interface = create_rpa_interface()

# スタンドアロン実行用
if __name__ == "__main__":
    print("🤖 RPA自動化システム起動中...")
    gradio_interface.launch(
        server_port=7865,
        share=False,
        debug=True
    )
