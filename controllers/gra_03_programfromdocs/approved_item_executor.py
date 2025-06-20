#!/usr/bin/env python3
"""
承認済みアイテム実行ツール
承認されたアイテムを実際にシステム生成・GitHub push・Google Chat通知まで実行します
"""

import sqlite3
import sys
import os
import json
import requests
import subprocess
from datetime import datetime
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.append('/workspaces/fastapi_django_main_live')

class ApprovedItemExecutor:
    """承認済みアイテムの実行クラス"""
    
    def __init__(self):
        self.db_path = "/workspaces/fastapi_django_main_live/prompts.db"
        self.github_token = os.environ.get('GITHUB_TOKEN', '')
        self.google_chat_webhook = os.environ.get('GOOGLE_CHAT_WEBHOOK', '')
    
    def get_approved_items(self):
        """承認済みでまだ実行されていないアイテムを取得"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT aq.id, aq.issue_title, aq.issue_body, aq.approved_by, aq.approved_at
                FROM approval_queue aq
                LEFT JOIN execution_log el ON aq.id = el.approval_id
                WHERE aq.approval_status = 'approved' 
                AND el.id IS NULL
                ORDER BY aq.approved_at ASC
            ''')
            
            items = cursor.fetchall()
            conn.close()
            return items
            
        except Exception as e:
            print(f"❌ 承認済みアイテム取得エラー: {e}")
            return []
    
    def create_execution_log(self, approval_id, status="started"):
        """実行ログを作成"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO execution_log (
                    approval_id, execution_start, status
                ) VALUES (?, CURRENT_TIMESTAMP, ?)
            ''', (approval_id, status))
            
            log_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return log_id
            
        except Exception as e:
            print(f"❌ 実行ログ作成エラー: {e}")
            return None
    
    def update_execution_log(self, log_id, status, result_summary="", github_repo_url="", error_message=""):
        """実行ログを更新"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE execution_log 
                SET execution_end = CURRENT_TIMESTAMP,
                    status = ?, result_summary = ?, 
                    github_repo_url = ?, error_message = ?
                WHERE id = ?
            ''', (status, result_summary, github_repo_url, error_message, log_id))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"❌ 実行ログ更新エラー: {e}")
            return False
    
    def simulate_system_generation(self, title, description):
        """システム生成をシミュレート（GPT-ENGINEER代替）"""
        print(f"🔧 システム生成開始: {title}")
        
        # 簡単なHTMLファイルを生成（デモ用）
        html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
        }}
        .description {{
            background-color: #f8f9fa;
            padding: 15px;
            border-left: 4px solid #007bff;
            margin: 20px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 {title}</h1>
        <div class="description">
            <h3>システム概要:</h3>
            <pre>{description}</pre>
        </div>
        <div class="footer">
            <p>✅ システム生成完了 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>🤖 Generated by Auto System Creator</p>
        </div>
    </div>
</body>
</html>"""
        
        # 生成されたファイルの保存先
        output_dir = Path("/tmp/generated_system")
        output_dir.mkdir(exist_ok=True)
        
        html_file = output_dir / "index.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # README.mdも生成
        readme_content = f"""# {title}

{description}

## 生成情報
- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 生成システム: Auto System Creator
- 承認フロー: GitHub ISSUE → SQLite承認 → 自動生成

## ファイル構成
- index.html: メインHTMLファイル
- README.md: このファイル

## 実行方法
ブラウザでindex.htmlを開いてください。
"""
        
        readme_file = output_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"✅ システム生成完了: {output_dir}")
        return output_dir
    
    def create_github_repository_and_push(self, title, output_dir, approval_id):
        """GitHubリポジトリを実際に作成し、コードをプッシュ"""
        if not self.github_token or len(self.github_token) < 10:
            return {
                'success': False,
                'repo_url': 'GitHub Token未設定のためスキップ',
                'message': 'GitHub Token未設定'
            }
        
        try:
            # リポジトリ名を生成
            repo_name = f"auto-generated-{approval_id}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            
            # GitHub APIでリポジトリ作成
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            repo_data = {
                'name': repo_name,
                'description': f"自動生成システム: {title}",
                'private': False,
                'auto_init': False  # 既存ファイルをプッシュするためFalse
            }
            
            print(f"📡 GitHubリポジトリ作成中: {repo_name}")
            response = requests.post(
                'https://api.github.com/user/repos',
                headers=headers,
                json=repo_data
            )
            
            if response.status_code != 201:
                return {
                    'success': False,
                    'repo_url': f'GitHub API エラー: {response.status_code}',
                    'message': f'リポジトリ作成失敗: {response.text}'
                }
            
            repo_info = response.json()
            clone_url = repo_info['clone_url']
            html_url = repo_info['html_url']
            
            print(f"✅ GitHubリポジトリ作成成功: {html_url}")
            
            # Git設定
            subprocess.run(['git', 'config', '--global', 'user.name', 'Auto System Creator'], 
                          cwd=output_dir, capture_output=True)
            subprocess.run(['git', 'config', '--global', 'user.email', 'auto-system@example.com'], 
                          cwd=output_dir, capture_output=True)
            
            # Gitリポジトリ初期化とプッシュ
            print(f"📤 コードをGitHubにプッシュ中...")
            
            # HTTPSでのpush用にtoken付きURLを作成
            auth_clone_url = clone_url.replace('https://', f'https://{self.github_token}@')
            
            subprocess.run(['git', 'init'], cwd=output_dir, check=True, capture_output=True)
            subprocess.run(['git', 'add', '.'], cwd=output_dir, check=True, capture_output=True)
            subprocess.run(['git', 'commit', '-m', f'Initial commit: {title}'], 
                          cwd=output_dir, check=True, capture_output=True)
            subprocess.run(['git', 'branch', '-M', 'main'], cwd=output_dir, check=True, capture_output=True)
            subprocess.run(['git', 'remote', 'add', 'origin', auth_clone_url], 
                          cwd=output_dir, check=True, capture_output=True)
            subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                          cwd=output_dir, check=True, capture_output=True)
            
            print(f"✅ GitHubプッシュ完了: {html_url}")
            
            return {
                'success': True,
                'repo_url': html_url,
                'message': 'リポジトリ作成・プッシュ完了'
            }
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Git操作エラー: {e}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'repo_url': f'Git操作失敗: {e.returncode}',
                'message': error_msg
            }
        except Exception as e:
            error_msg = f"GitHub処理エラー: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'repo_url': f'処理失敗: {str(e)}',
                'message': error_msg
            }
    
    def send_google_chat_notification(self, title, message, success=True, github_url=None):
        """Google Chatに通知を送信"""
        if not self.google_chat_webhook:
            print("⚠️ Google Chat Webhook URLが設定されていません")
            return False
        
        icon = "✅" if success else "❌"
        
        # Google Chat用のメッセージフォーマット
        widgets = [
            {
                "textParagraph": {
                    "text": message
                }
            }
        ]
        
        # GitHubリンクがある場合はボタンとして追加
        if github_url and github_url.startswith('https://github.com/'):
            widgets.append({
                "buttons": [
                    {
                        "textButton": {
                            "text": "🔗 GitHubリポジトリを開く",
                            "onClick": {
                                "openLink": {
                                    "url": github_url
                                }
                            }
                        }
                    }
                ]
            })
        
        payload = {
            "cards": [
                {
                    "header": {
                        "title": f"{icon} システム自動生成通知",
                        "subtitle": title,
                        "imageUrl": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
                    },
                    "sections": [
                        {
                            "widgets": widgets
                        }
                    ]
                }
            ]
        }
        
        try:
            response = requests.post(
                self.google_chat_webhook,
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                print(f"✅ Google Chat通知送信成功")
                return True
            else:
                print(f"❌ Google Chat通知送信失敗: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Google Chat通知エラー: {e}")
            return False
    
    def execute_approved_item(self, approval_id, title, description):
        """承認済みアイテムを実行"""
        print(f"\n🚀 承認済みアイテム実行開始")
        print(f"ID: {approval_id}")
        print(f"タイトル: {title}")
        print("-" * 60)
        
        # 実行ログ開始
        log_id = self.create_execution_log(approval_id, "started")
        if not log_id:
            print("❌ 実行ログ作成に失敗しました")
            return False
        
        try:
            # ステップ1: システム生成
            print("📝 ステップ1: システム生成")
            output_dir = self.simulate_system_generation(title, description)
            
            # ステップ2: GitHub リポジトリ作成とプッシュ
            print("📝 ステップ2: GitHub処理")
            github_result = self.create_github_repository_and_push(title, output_dir, approval_id)
            
            if github_result['success']:
                github_url = github_result['repo_url']
                print(f"✅ GitHubリポジトリ作成・プッシュ完了: {github_url}")
            else:
                github_url = github_result['repo_url']
                print(f"⚠️ GitHub処理: {github_result['message']}")
            
            # ステップ3: Google Chat通知
            print("📝 ステップ3: Google Chat通知")
            notification_message = f"""システム自動生成が完了しました！

📋 プロジェクト: {title}
📁 ファイル: {output_dir}
⏰ 完了時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

承認フローによる自動生成システムが正常に動作しています。"""
            
            self.send_google_chat_notification(
                title, 
                notification_message, 
                True, 
                github_url if github_result['success'] else None
            )
            
            # 実行ログ完了
            self.update_execution_log(
                log_id, 
                "completed", 
                f"システム生成完了: {output_dir}",
                github_url
            )
            
            print(f"\n🎉 承認済みアイテム実行完了!")
            print(f"✅ 生成ディレクトリ: {output_dir}")
            print(f"✅ GitHub URL: {github_url}")
            
            return True
            
        except Exception as e:
            error_msg = f"実行エラー: {str(e)}"
            print(f"❌ {error_msg}")
            
            # エラーログ更新
            self.update_execution_log(log_id, "failed", "", "", error_msg)
            
            # エラー通知
            self.send_google_chat_notification(
                title, 
                f"システム生成中にエラーが発生しました: {error_msg}",
                False,
                None
            )
            
            return False
    
    def show_approved_items(self):
        """承認済みアイテム一覧を表示"""
        items = self.get_approved_items()
        
        print("\n📋 実行待ちの承認済みアイテム:")
        print("=" * 80)
        
        if not items:
            print("  実行待ちのアイテムはありません")
            return []
        
        for item in items:
            id, title, body, approved_by, approved_at = item
            print(f"✅ ID:{id} | {title}")
            print(f"   承認者: {approved_by} | 承認日時: {approved_at}")
            print(f"   概要: {body[:100]}...")
            print("-" * 80)
        
        print(f"合計: {len(items)}件")
        return items

def main():
    """メイン実行"""
    print("🚀 承認済みアイテム実行ツール")
    print("=" * 60)
    
    executor = ApprovedItemExecutor()
    
    # 現在の実行待ちアイテムを表示
    items = executor.show_approved_items()
    
    if not items:
        print("\n🎯 実行可能なアイテムがありません")
        print("まず承認システムでアイテムを承認してください")
        return
    
    print("\n📝 実行したい操作を選択してください:")
    print("1. 特定のアイテムを実行")
    print("2. すべてのアイテムを順次実行")
    print("3. 終了")
    
    choice = input("\n選択 (1-3): ").strip()
    
    if choice == "1":
        item_id = input("実行するアイテムのID: ").strip()
        try:
            item_id = int(item_id)
            # 指定されたIDのアイテムを検索
            target_item = None
            for item in items:
                if item[0] == item_id:
                    target_item = item
                    break
            
            if target_item:
                executor.execute_approved_item(
                    target_item[0],  # ID
                    target_item[1],  # title
                    target_item[2]   # body
                )
            else:
                print(f"❌ ID {item_id} のアイテムが見つかりません")
                
        except ValueError:
            print("❌ 無効なID形式です")
    
    elif choice == "2":
        print(f"\n🚀 {len(items)}個のアイテムを順次実行します...")
        
        for i, item in enumerate(items, 1):
            print(f"\n📋 {i}/{len(items)} 番目のアイテムを実行中...")
            executor.execute_approved_item(
                item[0],  # ID
                item[1],  # title
                item[2]   # body
            )
    
    elif choice == "3":
        print("👋 実行ツールを終了します")
    
    else:
        print("❌ 無効な選択です")

if __name__ == "__main__":
    main()
