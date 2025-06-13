# Technical Deep Dive: RPA + AI Debug System

## 🔧 Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Gradio UI     │───▶│ RPA Manager     │───▶│ Screenshot      │
│   Interface     │    │ (Selenium)      │    │ Capture         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ AI Analysis     │◀───│ Debug System    │───▶│ History Storage │
│ Prompt Gen      │    │ Orchestrator    │    │ (JSON/SQLite)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 💻 Core Implementation

### 1. Main System Class

```python
class RPADebugSystem:
    """
    統合デバッグシステムの中核クラス
    RPA、AI分析、履歴管理を統合
    """
    
    def __init__(self):
        # RPA Manager初期化
        if RPA_AVAILABLE:
            self.rpa_manager = RPAManager()
        else:
            self.rpa_manager = None
        
        # デバッグ履歴とファイルパス管理
        self.debug_history = []
        self.capture_dir = Path("/workspaces/fastapi_django_main_live/docs/images/debug_captures")
        self.capture_dir.mkdir(parents=True, exist_ok=True)
    
    async def capture_and_analyze(self, url: str, description: str = "", selector: str = None) -> tuple:
        """
        メインワークフロー:
        1. RPA自動キャプチャ
        2. ファイル保存
        3. AI分析プロンプト生成
        4. 履歴記録
        
        Returns:
            (PIL.Image, analysis_prompt, file_path)
        """
        if not self.rpa_manager:
            return None, "❌ RPA機能が利用できません", ""
        
        try:
            # 🤖 RPA実行: スクリーンショット取得
            img, capture_message = await self.rpa_manager.capture_screenshot(
                url=url,
                selector=selector,
                wait_time=5  # エラー画面読み込み待機
            )
            
            if not img:
                return None, f"❌ キャプチャ失敗: {capture_message}", ""
            
            # 💾 ファイル保存: タイムスタンプ + セレクター情報
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            selector_suffix = f"_selector" if selector else "_fullpage"
            filename = f"debug_capture_{timestamp}{selector_suffix}.png"
            capture_path = self.capture_dir / filename
            img.save(capture_path)
            
            # 🧠 AI分析プロンプト生成
            analysis_prompt = self._generate_analysis_prompt(description, selector)
            
            # 📊 履歴記録
            debug_record = {
                "timestamp": datetime.now().isoformat(),
                "url": url,
                "description": description,
                "selector": selector,
                "capture_path": str(capture_path),
                "analysis_prompt": analysis_prompt
            }
            self.debug_history.append(debug_record)
            
            return img, analysis_prompt, str(capture_path)
            
        except Exception as e:
            error_msg = f"❌ キャプチャ・解析エラー: {str(e)}"
            return None, error_msg, ""
```

### 2. AI Prompt Engineering

```python
def _generate_analysis_prompt(self, description: str, selector: str = None) -> str:
    """
    Gradio特化のAI分析プロンプト生成
    構造化された出力形式でデバッグ効率を最大化
    """
    
    base_prompt = """
🔍 **RPA キャプチャ画像解析 - Gradio アプリケーション専用**

この画像はGradioベースのWebアプリケーションのキャプチャです。以下の点を重点的に分析してください：

## 📋 **Gradio特有の解析項目**
1. **エラーメッセージの特定**
   - Gradio エラーダイアログ
   - Python トレースバック表示
   - 赤いエラーバナー
   - "Error" や "Exception" の文字

2. **Gradio UI要素の状態**
   - タブの選択状態とエラー表示
   - ボタンの有効/無効状態
   - 入力フィールドのエラー状態
   - プログレスバーの状態

3. **アプリケーション状態**
   - "Running on..." メッセージ
   - 読み込み中インジケーター
   - 接続エラーメッセージ
   - JavaScript console エラー

4. **タブとインターフェース**
   - どのタブが選択されているか
   - エラーが発生しているタブ
   - インターフェースの表示状態

5. **改善提案**
   - Gradio特有のエラー対処法
   - Python/FastAPI の修正点
   - 環境設定の問題"""
    
    # セレクター特化分析
    if selector:
        base_prompt += f"""

## 🎯 **セレクター指定キャプチャ**
**対象セレクター**: `{selector}`
この特定の要素に焦点を当てて、その部分の問題を詳細に分析してください。
"""
    
    # ユーザー問題説明の統合
    if description:
        base_prompt += f"""

## 👤 **ユーザー報告内容**
**問題の詳細**: {description}
上記の説明を踏まえて、特にその点に関連する問題を重点的に分析してください。
"""
    
    # 構造化出力フォーマット
    base_prompt += """

## 📊 **出力形式**
- 🚨 **問題の種類**: Gradioエラー / Pythonエラー / UI問題 / 接続問題
- 🔴 **重要度**: 高 / 中 / 低
- ⭐ **難易度**: 簡単 / 中程度 / 困難
- ⏱️ **推定解決時間**: 具体的な時間
- 🛠️ **修正手順**: ステップバイステップの説明
- 💡 **根本原因**: 技術的な原因の特定

Gradioアプリケーションに特化した実用的な分析をお願いします！
"""
    
    return base_prompt
```

### 3. Gradio Interface Implementation

```python
def create_rpa_debug_interface():
    """
    ユーザーフレンドリーなGradioインターフェース
    デュアルキャプチャモード + リアルタイム解析
    """
    
    debug_system = RPADebugSystem()
    
    def capture_and_analyze_wrapper(url, description, selector=None):
        """非同期関数の同期ラッパー"""
        if not url:
            return None, "❌ URLを入力してください", "", ""
        
        try:
            # asyncio.run()で非同期関数を同期実行
            img, analysis_result, capture_path = asyncio.run(
                debug_system.capture_and_analyze(url, description, selector)
            )
            
            history = debug_system.get_debug_history()
            return img, analysis_result, capture_path, history
            
        except Exception as e:
            error_msg = f"❌ エラー: {str(e)}"
            return None, error_msg, "", debug_system.get_debug_history()
    
    # 🎨 UI Layout Design
    with gr.Blocks(title="🔍 RPA + AI デバッグ", theme="soft") as interface:
        gr.Markdown("# 🔍 RPA + AI 画像解析デバッグシステム")
        gr.Markdown("""
        **RPAでキャプチャ → AI解析 → エラー特定・解決策提案**の統合システム
        
        実際の業務ソフトの画面をキャプチャして、AIが問題を特定・解決策を提案します。
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                # 📸 キャプチャ設定セクション
                gr.Markdown("## 📸 キャプチャ設定")
                
                url_input = gr.Textbox(
                    label="🌐 対象URL",
                    placeholder="https://example.com または http://localhost:7860",
                    value="https://ideal-halibut-4q5qp79g2jp9-7860.app.github.dev/"
                )
                
                selector_input = gr.Textbox(
                    label="🎯 セレクター (オプション)",
                    placeholder="例: .gradio-container, #app, .error-message",
                    info="特定の要素のみキャプチャしたい場合はCSSセレクターを入力"
                )
                
                description_input = gr.Textbox(
                    label="📝 問題・状況の説明",
                    placeholder="どのような問題が発生していますか？",
                    lines=3
                )
                
                # 🔘 デュアルキャプチャボタン
                with gr.Row():
                    capture_btn = gr.Button("📸 全画面キャプチャ", variant="primary")
                    capture_selector_btn = gr.Button("🎯 セレクター指定キャプチャ", variant="secondary")
        
        # 🎯 イベントハンドラー設定
        capture_btn.click(
            fn=lambda url, desc: capture_and_analyze_wrapper(url, desc, None),
            inputs=[url_input, description_input],
            outputs=[captured_image, analysis_result, capture_info, debug_history]
        )
        
        capture_selector_btn.click(
            fn=lambda url, desc, sel: capture_and_analyze_wrapper(url, desc, sel),
            inputs=[url_input, description_input, selector_input],
            outputs=[captured_image, analysis_result, capture_info, debug_history]
        )
    
    return interface
```

## 🧪 Automated Testing System

### Jupyter Notebook Test Framework

```python
# rpa_capture_test.ipynb の主要クラス

class CaptureConfig:
    """キャプチャ設定の管理クラス"""
    def __init__(self):
        self.base_url = "https://ideal-halibut-4q5qp79g2jp9-7860.app.github.dev/"
        self.selectors = [
            ".gradio-container",
            "button[data-testid='tab-button']",
            ".gr-error",
            "#app"
        ]
        self.descriptions = [
            "メインコンテナの表示確認",
            "タブボタンの状態チェック", 
            "エラーメッセージの検出",
            "アプリケーション全体の状態"
        ]

class AutoCaptureSystem:
    """自動化テストシステム"""
    
    def __init__(self, config: CaptureConfig):
        self.config = config
        self.debug_system = RPADebugSystem()
        self.results = []
    
    async def run_capture_test(self, test_name: str = "auto_test"):
        """バッチキャプチャテストの実行"""
        
        # サーバー状態確認
        if not await self.check_server_status():
            return False, "Server is not accessible"
        
        # 複数パターンのテスト実行
        for i, (selector, description) in enumerate(zip(
            self.config.selectors, 
            self.config.descriptions
        )):
            print(f"📸 Test {i+1}/{len(self.config.selectors)}: {description}")
            
            try:
                img, analysis, path = await self.debug_system.capture_and_analyze(
                    url=self.config.base_url,
                    description=f"[{test_name}] {description}",
                    selector=selector
                )
                
                if img:
                    self.results.append({
                        "test_id": f"{test_name}_{i+1}",
                        "selector": selector,
                        "success": True,
                        "path": path,
                        "size": f"{img.size[0]}x{img.size[1]}"
                    })
                    print(f"  ✅ Success: {Path(path).name}")
                else:
                    print(f"  ❌ Failed: {analysis}")
                
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
        
        return True, f"Completed {len(self.results)} captures"
    
    async def check_server_status(self) -> bool:
        """サーバー接続確認"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(self.config.base_url, timeout=10) as response:
                    return response.status == 200
        except:
            return False
```

## 🔍 Error Handling Patterns

### 1. Graceful Degradation

```python
# RPA機能の優雅なフォールバック
try:
    from contbk.gra_12_rpa.rpa_automation import RPAManager
    RPA_AVAILABLE = True
except ImportError:
    RPA_AVAILABLE = False
    print("⚠️ RPA機能が利用できません")

# 条件付き機能提供
if not self.rpa_manager:
    return None, "❌ RPA機能が利用できません", ""
```

### 2. Comprehensive Exception Handling

```python
async def capture_and_analyze(self, url: str, description: str = "", selector: str = None):
    try:
        # メイン処理
        img, capture_message = await self.rpa_manager.capture_screenshot(...)
        
        if not img:
            return None, f"❌ キャプチャ失敗: {capture_message}", ""
        
        # 成功処理
        return img, analysis_prompt, str(capture_path)
        
    except Exception as e:
        # 統一されたエラーフォーマット
        error_msg = f"❌ キャプチャ・解析エラー: {str(e)}"
        return None, error_msg, ""
```

### 3. Input Validation

```python
def capture_and_analyze_wrapper(url, description, selector=None):
    """入力検証付きラッパー関数"""
    
    # URL必須チェック
    if not url:
        return None, "❌ URLを入力してください", "", ""
    
    # セレクター検証（セレクター指定モード時）
    if selector is not None and not selector.strip():
        return None, "❌ セレクターを入力してください", "", ""
    
    # メイン処理実行
    return asyncio.run(debug_system.capture_and_analyze(url, description, selector))
```

## 📊 Performance Metrics

### Capture Performance
- **Full Page**: ~3-5秒
- **Selector Specific**: ~2-3秒  
- **Error Recovery**: ~1秒

### Storage Efficiency
- **Image Format**: PNG (可逆圧縮)
- **Naming Convention**: `debug_capture_YYYYMMDD_HHMMSS_[fullpage|selector].png`
- **Average Size**: 200-800KB per capture

### Memory Management
- **PIL Image Objects**: 自動ガベージコレクション
- **History Limit**: 最新10件表示（メモリ効率化）
- **File Cleanup**: 手動管理（将来の自動化対象）

## 🔧 CSS Selector Patterns

### Gradio-Specific Selectors

```css
/* メインコンテナ */
.gradio-container
#app

/* タブシステム */
button[data-testid="tab-button"]
.tab-nav button:nth-child(2)

/* エラー表示 */
.gr-error
.error-message  
.gradio-error

/* 入力フィールド */
.gr-textbox
input[type="text"]
textarea.gr-textarea

/* ボタン */
.gr-button
button.primary
button.secondary

/* 特定コンポーネント */
#component-123
.gr-interface:nth-child(3)
```

## 🚀 Deployment Strategy

### Local Development
```bash
# 開発環境での実行
python rpa_ai_debug_system.py
# → http://localhost:7866
```

### Integration Mode  
```python
# メインアプリケーションへの統合
# app.py に自動追加される新タブとして
interface_title = "🔍 RPA + AI デバッグ"
```

### Testing Mode
```bash
# Jupyter Notebook実行
jupyter notebook rpa_capture_test.ipynb
```

---

**This technical documentation demonstrates advanced integration of RPA, AI, and modern web frameworks for practical debugging automation.**
