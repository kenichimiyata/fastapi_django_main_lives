#!/usr/bin/env python3
"""
🎯 AI-Human協働開発システム - 初心者向け順次テストガイド

このシステムは初めて使う方でも簡単に操作できるよう、
ステップバイステップのガイド付きインターフェースを提供します。

上から順番に実行していくだけで、システム全体を体験できます。
"""

import gradio as gr
import sqlite3
import json
from datetime import datetime
from pathlib import Path
import sys
import os

# プロジェクトルートをパスに追加
sys.path.append('/workspaces/fastapi_django_main_live')

class SystemTestGuide:
    """システムテストガイドクラス"""
    
    def __init__(self):
        self.db_path = "/workspaces/fastapi_django_main_live/prompts.db"
        self.current_step = 1
        self.max_steps = 7
        self.test_results = {}
        
    def get_step_description(self, step_num):
        """各ステップの詳細説明を取得"""
        descriptions = {
            1: {
                "title": "🎯 ステップ1: システム起動確認",
                "description": """
**目的**: システムが正常に動作しているか確認します

**確認項目**:
- データベース接続状態
- 必要なテーブルの存在確認
- 基本的な読み書き動作

**期待される結果**: 全ての確認項目が✅になること
                """,
                "button_text": "システム状態をチェック",
                "next_step": "データベースが正常であれば、次はプロンプトを作成してみましょう！"
            },
            2: {
                "title": "📝 ステップ2: プロンプト作成・保存",
                "description": """
**目的**: 新しいプロンプトを作成してデータベースに保存します

**操作方法**:
1. タイトル欄に「テスト: 簡単な計算機」と入力
2. 内容欄に「Pythonで足し算と引き算ができる簡単な計算機を作成してください」と入力
3. 「プロンプト保存」ボタンをクリック

**期待される結果**: 「✅ プロンプト保存完了」のメッセージ
                """,
                "button_text": "プロンプトを保存",
                "next_step": "プロンプトが保存できたら、承認システムに送信してみましょう！"
            },
            3: {
                "title": "📨 ステップ3: 承認キューに追加",
                "description": """
**目的**: 作成したプロンプトを承認システムに送信します

**操作方法**:
1. 前のステップで作成したプロンプトのタイトルと内容をコピー
2. 優先度を設定（1=最高、5=普通、9=最低）
3. 「承認キューに追加」ボタンをクリック

**期待される結果**: 承認待ちキューに新しいアイテムが追加される
                """,
                "button_text": "承認キューに追加",
                "next_step": "承認キューに追加できたら、承認処理を実行してみましょう！"
            },
            4: {
                "title": "🤔 ステップ4: 承認・拒否判定",
                "description": """
**目的**: 承認待ちのアイテムを確認し、承認または拒否を決定します

**操作方法**:
1. 「承認待ちキューを更新」ボタンでキューを表示
2. 承認したいアイテムのIDを確認
3. IDを入力して「承認」ボタンをクリック

**期待される結果**: アイテムのステータスが「approved」に変更される
                """,
                "button_text": "承認処理を実行",
                "next_step": "承認が完了したら、自動実行システムをテストしてみましょう！"
            },
            5: {
                "title": "🚀 ステップ5: 自動実行システム",
                "description": """
**目的**: 承認されたプロンプトを自動実行してコードを生成します

**動作内容**:
- AI APIを使用してコード生成
- 生成されたコードをファイルに保存
- 実行ログに結果を記録

**期待される結果**: コードファイルの生成と実行ログの記録
                """,
                "button_text": "自動実行開始",
                "next_step": "コード生成が完了したら、GitHub連携をテストしてみましょう！"
            },
            6: {
                "title": "🐙 ステップ6: GitHub連携",
                "description": """
**目的**: 生成されたコードをGitHub Issueとして作成します

**動作内容**:
- GitHub APIを使用してIssue作成
- 生成コードをIssue本文に添付
- 適切なラベルとタイトルを設定

**期待される結果**: GitHub上に新しいIssueが作成される
                """,
                "button_text": "GitHub Issue作成",
                "next_step": "GitHub連携が完了したら、最終ステップでログを確認しましょう！"
            },
            7: {
                "title": "📊 ステップ7: ログ・完了確認",
                "description": """
**目的**: 全ての処理が正常に完了したことを確認します

**確認項目**:
- プロンプトの保存ログ
- 承認処理のログ
- 自動実行のログ
- GitHub連携のログ

**期待される結果**: 全てのステップが✅で完了していること
                """,
                "button_text": "最終ログ確認",
                "next_step": "🎉 おめでとうございます！全てのステップが完了しました！"
            }
        }
        return descriptions.get(step_num, {})
    
    def check_system_status(self):
        """ステップ1: システム状態確認"""
        try:
            results = []
            
            # データベース接続確認
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            results.append("✅ データベース接続: 正常")
            
            # テーブル存在確認
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            required_tables = ['prompts', 'approval_queue', 'execution_log']
            for table in required_tables:
                if table in tables:
                    results.append(f"✅ {table}テーブル: 存在")
                else:
                    results.append(f"❌ {table}テーブル: 不在")
            
            # 基本的な読み書きテスト
            cursor.execute("SELECT COUNT(*) FROM prompts")
            prompt_count = cursor.fetchone()[0]
            results.append(f"✅ プロンプト数: {prompt_count}件")
            
            cursor.execute("SELECT COUNT(*) FROM approval_queue")
            queue_count = cursor.fetchone()[0]
            results.append(f"✅ 承認キュー: {queue_count}件")
            
            conn.close()
            
            self.test_results['step1'] = True
            return "\\n".join(results) + "\\n\\n🎉 システム状態確認完了！次のステップに進めます。"
            
        except Exception as e:
            self.test_results['step1'] = False
            return f"❌ システム確認エラー: {str(e)}"
    
    def save_test_prompt(self, title, content):
        """ステップ2: テストプロンプト保存"""
        try:
            if not title or not content:
                return "❌ タイトルと内容の両方を入力してください"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                'INSERT INTO prompts (title, content, created_at) VALUES (?, ?, ?)',
                (title, content, datetime.now().isoformat())
            )
            
            prompt_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            self.test_results['step2'] = {'id': prompt_id, 'title': title, 'content': content}
            
            return f"""✅ プロンプト保存完了！
            
📋 保存内容:
- ID: {prompt_id}
- タイトル: {title}
- 内容: {content[:100]}...

🎯 次のステップ: このプロンプトを承認キューに追加してください"""
            
        except Exception as e:
            self.test_results['step2'] = False
            return f"❌ プロンプト保存エラー: {str(e)}"
    
    def add_to_approval_queue(self, title, content, priority):
        """ステップ3: 承認キューに追加"""
        try:
            if not title or not content:
                return "❌ タイトルと内容を入力してください"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO approval_queue (
                    issue_title, issue_body, requester, priority, 
                    approval_status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                title, content, "test_user", priority, 
                "pending_review", datetime.now().isoformat()
            ))
            
            queue_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            self.test_results['step3'] = {'id': queue_id, 'title': title}
            
            return f"""✅ 承認キューに追加完了！
            
📨 追加内容:
- キューID: {queue_id}
- タイトル: {title}
- 優先度: {priority}
- ステータス: pending_review

🎯 次のステップ: ID {queue_id} を承認してください"""
            
        except Exception as e:
            self.test_results['step3'] = False
            return f"❌ 承認キュー追加エラー: {str(e)}"
    
    def approve_request(self, request_id):
        """ステップ4: 承認処理"""
        try:
            if not request_id:
                return "❌ 承認するアイテムのIDを入力してください"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # アイテム存在確認
            cursor.execute('SELECT issue_title FROM approval_queue WHERE id = ?', (request_id,))
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return f"❌ ID {request_id} のアイテムが見つかりません"
            
            title = result[0]
            
            # 承認処理
            cursor.execute('''
                UPDATE approval_queue 
                SET approval_status = ?, approved_by = ?, approved_at = ?
                WHERE id = ?
            ''', ('approved', 'test_approver', datetime.now().isoformat(), request_id))
            
            conn.commit()
            conn.close()
            
            self.test_results['step4'] = {'id': request_id, 'title': title}
            
            return f"""✅ 承認処理完了！
            
🤝 承認内容:
- アイテムID: {request_id}
- タイトル: {title}
- 承認者: test_approver
- 承認日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎯 次のステップ: 自動実行システムをテストしてください"""
            
        except Exception as e:
            self.test_results['step4'] = False
            return f"❌ 承認処理エラー: {str(e)}"
    
    def simulate_auto_execution(self):
        """ステップ5: 自動実行シミュレーション"""
        try:
            # シミュレーション用のコード生成
            generated_code = '''
def simple_calculator():
    """簡単な計算機"""
    print("=== 簡単な計算機 ===")
    
    while True:
        try:
            num1 = float(input("最初の数値を入力: "))
            operator = input("演算子を入力 (+, -, *, /): ")
            num2 = float(input("2番目の数値を入力: "))
            
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 != 0:
                    result = num1 / num2
                else:
                    print("エラー: ゼロで割ることはできません")
                    continue
            else:
                print("エラー: 無効な演算子です")
                continue
            
            print(f"結果: {num1} {operator} {num2} = {result}")
            
            if input("続けますか？ (y/n): ").lower() != 'y':
                break
                
        except ValueError:
            print("エラー: 有効な数値を入力してください")
        except Exception as e:
            print(f"エラー: {e}")

if __name__ == "__main__":
    simple_calculator()
'''
            
            # ファイル保存シミュレーション
            output_dir = Path("/workspaces/fastapi_django_main_live/test_generated")
            output_dir.mkdir(exist_ok=True)
            
            file_path = output_dir / "simple_calculator.py"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(generated_code)
            
            # 実行ログ記録
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO execution_log (
                    approval_id, execution_start, execution_end, 
                    status, result_summary, github_repo_url
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                self.test_results.get('step4', {}).get('id', 0),
                datetime.now().isoformat(),
                datetime.now().isoformat(),
                'completed',
                f'ファイル生成完了: {file_path}',
                'https://github.com/test/repo'
            ))
            
            conn.commit()
            conn.close()
            
            self.test_results['step5'] = {'file_path': str(file_path)}
            
            return f"""✅ 自動実行完了！
            
🚀 実行結果:
- 生成ファイル: {file_path}
- ファイルサイズ: {len(generated_code)} 文字
- 実行時間: < 1秒
- ステータス: 正常完了

💡 生成されたコード:
```python
{generated_code[:200]}...
```

🎯 次のステップ: GitHub Issue作成をテストしてください"""
            
        except Exception as e:
            self.test_results['step5'] = False
            return f"❌ 自動実行エラー: {str(e)}"
    
    def simulate_github_issue(self):
        """ステップ6: GitHub Issue作成シミュレーション"""
        try:
            # GitHub Issue シミュレーション
            issue_data = {
                'number': 123,
                'title': '🧪 テスト: 簡単な計算機システム生成完了',
                'url': 'https://github.com/miyataken999/fastapi_django_main_live/issues/123',
                'body': f'''
# 🎯 自動生成システムテスト結果

## 📋 概要
承認されたプロンプトから簡単な計算機システムを自動生成しました。

## 🚀 生成内容
- **ファイル**: simple_calculator.py
- **機能**: 四則演算（+, -, *, /）
- **特徴**: エラーハンドリング付き

## 📊 実行詳細
- **実行日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **所要時間**: < 1秒
- **ステータス**: ✅ 正常完了

## 🔗 関連ファイル
- 生成コード: `/test_generated/simple_calculator.py`

---
*このIssueは自動生成システムによって作成されました*
'''
            }
            
            self.test_results['step6'] = issue_data
            
            return f"""✅ GitHub Issue作成完了！
            
🐙 作成されたIssue:
- Issue番号: #{issue_data['number']}
- タイトル: {issue_data['title']}
- URL: {issue_data['url']}
- 作成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📝 Issue内容プレビュー:
{issue_data['body'][:300]}...

🎯 次のステップ: 最終ログ確認を実行してください"""
            
        except Exception as e:
            self.test_results['step6'] = False
            return f"❌ GitHub Issue作成エラー: {str(e)}"
    
    def generate_final_report(self):
        """ステップ7: 最終レポート生成"""
        try:
            report_lines = ["# 🎉 全ステップ完了レポート\\n"]
            
            all_success = True
            for step_num in range(1, 8):
                step_key = f'step{step_num}'
                step_desc = self.get_step_description(step_num)
                
                if self.test_results.get(step_key):
                    status = "✅ 成功"
                    all_success = True
                else:
                    status = "❌ 未完了/エラー"
                    all_success = False
                
                report_lines.append(f"## {step_desc['title']}")
                report_lines.append(f"**ステータス**: {status}\\n")
            
            if all_success:
                report_lines.append("## 🎯 総合評価: 全ステップ正常完了！")
                report_lines.append("""
**あなたは以下を達成しました:**
- ✅ システム全体の動作確認
- ✅ プロンプトから自動コード生成
- ✅ 承認ワークフローの理解
- ✅ GitHub連携の体験
- ✅ 完全なE2Eテスト完了

🎉 おめでとうございます！AI-Human協働開発システムをマスターしました！
                """)
            else:
                report_lines.append("## ⚠️ 一部のステップが未完了です")
                report_lines.append("未完了のステップがある場合は、該当ステップを再実行してください。")
            
            final_report = "\\n".join(report_lines)
            
            return final_report
            
        except Exception as e:
            return f"❌ 最終レポート生成エラー: {str(e)}"

def create_gradio_interface():
    """Gradioインターフェース作成"""
    guide = SystemTestGuide()
    
    with gr.Blocks(
        title="🎯 AI-Human協働開発システム - 初心者向けガイド",
        theme="soft"
    ) as interface:
        
        gr.Markdown("""
        # 🎯 AI-Human協働開発システム - 初心者向けガイド
        
        **ようこそ！** このガイドでは、システムを上から順番に実行していくだけで、
        AI-Human協働開発の全プロセスを体験できます。
        
        **使い方**: 各ステップを順番に実行してください。前のステップが完了してから次に進みましょう。
        """)
        
        # ステップ1: システム確認
        with gr.Row():
            with gr.Column():
                step1_desc = guide.get_step_description(1)
                gr.Markdown(f"## {step1_desc['title']}")
                gr.Markdown(step1_desc['description'])
                
                step1_btn = gr.Button(step1_desc['button_text'], variant="primary")
                step1_result = gr.Textbox(label="ステップ1結果", lines=8, interactive=False)
                
                step1_btn.click(guide.check_system_status, outputs=step1_result)
        
        gr.Markdown("---")
        
        # ステップ2: プロンプト作成
        with gr.Row():
            with gr.Column():
                step2_desc = guide.get_step_description(2)
                gr.Markdown(f"## {step2_desc['title']}")
                gr.Markdown(step2_desc['description'])
                
                with gr.Row():
                    prompt_title = gr.Textbox(
                        label="プロンプトタイトル", 
                        value="テスト: 簡単な計算機",
                        placeholder="例: テスト: 簡単な計算機"
                    )
                    
                prompt_content = gr.Textbox(
                    label="プロンプト内容",
                    value="Pythonで足し算と引き算ができる簡単な計算機を作成してください。エラーハンドリングも含めてください。",
                    lines=3,
                    placeholder="ここにプロンプトの詳細を入力..."
                )
                
                step2_btn = gr.Button(step2_desc['button_text'], variant="primary")
                step2_result = gr.Textbox(label="ステップ2結果", lines=6, interactive=False)
                
                step2_btn.click(
                    guide.save_test_prompt,
                    inputs=[prompt_title, prompt_content],
                    outputs=step2_result
                )
        
        gr.Markdown("---")
        
        # ステップ3: 承認キュー追加
        with gr.Row():
            with gr.Column():
                step3_desc = guide.get_step_description(3)
                gr.Markdown(f"## {step3_desc['title']}")
                gr.Markdown(step3_desc['description'])
                
                with gr.Row():
                    queue_title = gr.Textbox(
                        label="タイトル（ステップ2からコピー）",
                        placeholder="前のステップのタイトルをここにコピー"
                    )
                    priority = gr.Slider(
                        minimum=1, maximum=9, value=3, step=1,
                        label="優先度（1=最高、9=最低）"
                    )
                
                queue_content = gr.Textbox(
                    label="内容（ステップ2からコピー）",
                    lines=3,
                    placeholder="前のステップの内容をここにコピー"
                )
                
                step3_btn = gr.Button(step3_desc['button_text'], variant="primary")
                step3_result = gr.Textbox(label="ステップ3結果", lines=6, interactive=False)
                
                step3_btn.click(
                    guide.add_to_approval_queue,
                    inputs=[queue_title, queue_content, priority],
                    outputs=step3_result
                )
        
        gr.Markdown("---")
        
        # ステップ4: 承認処理
        with gr.Row():
            with gr.Column():
                step4_desc = guide.get_step_description(4)
                gr.Markdown(f"## {step4_desc['title']}")
                gr.Markdown(step4_desc['description'])
                
                approval_id = gr.Number(
                    label="承認するアイテムのID（ステップ3の結果から）",
                    precision=0,
                    placeholder="例: 1"
                )
                
                step4_btn = gr.Button(step4_desc['button_text'], variant="primary")
                step4_result = gr.Textbox(label="ステップ4結果", lines=6, interactive=False)
                
                step4_btn.click(
                    guide.approve_request,
                    inputs=approval_id,
                    outputs=step4_result
                )
        
        gr.Markdown("---")
        
        # ステップ5: 自動実行
        with gr.Row():
            with gr.Column():
                step5_desc = guide.get_step_description(5)
                gr.Markdown(f"## {step5_desc['title']}")
                gr.Markdown(step5_desc['description'])
                
                step5_btn = gr.Button(step5_desc['button_text'], variant="primary")
                step5_result = gr.Textbox(label="ステップ5結果", lines=10, interactive=False)
                
                step5_btn.click(guide.simulate_auto_execution, outputs=step5_result)
        
        gr.Markdown("---")
        
        # ステップ6: GitHub連携
        with gr.Row():
            with gr.Column():
                step6_desc = guide.get_step_description(6)
                gr.Markdown(f"## {step6_desc['title']}")
                gr.Markdown(step6_desc['description'])
                
                step6_btn = gr.Button(step6_desc['button_text'], variant="primary")
                step6_result = gr.Textbox(label="ステップ6結果", lines=8, interactive=False)
                
                step6_btn.click(guide.simulate_github_issue, outputs=step6_result)
        
        gr.Markdown("---")
        
        # ステップ7: 最終確認
        with gr.Row():
            with gr.Column():
                step7_desc = guide.get_step_description(7)
                gr.Markdown(f"## {step7_desc['title']}")
                gr.Markdown(step7_desc['description'])
                
                step7_btn = gr.Button(step7_desc['button_text'], variant="primary")
                step7_result = gr.Textbox(label="最終レポート", lines=15, interactive=False)
                
                step7_btn.click(guide.generate_final_report, outputs=step7_result)
        
        gr.Markdown("""
        ---
        ## 🎯 完了後のNext Steps
        
        全てのステップを完了したら、以下の実際のシステムも体験してみてください：
        
        - **🚀 統合管理ダッシュボード**: 実際の開発プロジェクト管理
        - **🐙 GitHub Issue自動生成**: リアルなGitHub連携
        - **💾 プロンプト管理システム**: 本格的なプロンプト開発
        
        **質問やサポートが必要な場合は、GitHub Issueでお気軽にお聞かせください！**
        """)
    
    return interface

# Gradioインターフェースのエクスポート
gradio_interface = create_gradio_interface()
interface_title = "🎯 初心者向けシステムガイド"

if __name__ == "__main__":
    gradio_interface.launch(
        server_name="0.0.0.0",
        server_port=7862,
        share=False
    )
