import shutil
import gradio as gr
#from mysite.libs.utilities import chat_with_interpreter, completion, process_file
#from interpreter import interpreter
#import mysite.interpreter.interpreter_config  # インポートするだけで設定が適用されます
import importlib
import os
import pkgutil
#from babyagi.babyagi import gradio_babyagi
#from routers.gra_02_openInterpreter.OpenInterpreter import gradio_interface
#from llamafactory.webui.interface import create_ui
import importlib
import os
import pkgutil

import importlib
import os
import pkgutil
import traceback

def include_gradio_interfaces():
    gradio_interfaces = {}  # 辞書型: { interface_name: gradio_interface }
    
    # 検索対象ディレクトリを指定（ContBKは統合ダッシュボードで表示するため除外）
    search_dirs = [
        ("controllers", "controllers"),  # メインのcontrollersディレクトリのみ
    ]
    
    package_paths = []
    
    # 各検索ディレクトリをスキャン
    for package_dir, module_prefix in search_dirs:
        if os.path.exists(package_dir):
            print(f"📂 Scanning directory: {package_dir}")
            for root, dirs, files in os.walk(package_dir):
                if "__pycache__" in root:  # `__pycache__` を除外
                    continue
                package_paths.append((root, module_prefix))

    for package_path, module_prefix in package_paths:
        # パッケージの Python モジュールを取得
        rel_path = os.path.relpath(package_path, module_prefix.split('.')[0] if '.' in module_prefix else module_prefix)
        
        if rel_path == ".":
            package_name = module_prefix
        else:
            package_name = module_prefix + "." + rel_path.replace(os.sep, ".")

        for module_info in pkgutil.iter_modules([package_path]):
            sub_module_name = f"{package_name}.{module_info.name}"
            print(f"Trying to import {sub_module_name}")

            try:
                module = importlib.import_module(sub_module_name)
                print(f"Successfully imported {sub_module_name}")

                # `gradio_interface` を持つモジュールのみ追加
                if hasattr(module, "gradio_interface"):
                    print(f"Found gradio_interface in {sub_module_name}")

                    # 美しいタイトルを生成（絵文字付き）
                    base_name = module_info.name
                    
                    # 特定のモジュールに対する美しいタイトルマッピング
                    title_mapping = {
                        'beginner_guide_system': '🚀 初心者ガイド',
                        'conversation_history': '💬 会話履歴管理',
                        'conversation_logger': '📝 会話ログ',
                        'conversation_demo': '🎯 会話履歴統合デモ',
                        'contbk_unified_dashboard': '🎯 ContBK統合ダッシュボード',
                        # 'contbk_example': '🎯 ContBK ダッシュボード',  # 無効化済み
                        # 'contbk_dashboard': '📊 ContBK 統合',  # 無効化済み
                        # 'example_gradio_interface': '🔧 サンプル',  # 無効化済み
                        'hasura': '🗄️ Hasura API',
                        'Chat': '💬 チャット',
                        'OpenInterpreter': '🤖 AI インタープリター',
                        'programfromdoc': '📄 ドキュメント生成',
                        'gradio_interface': '🚀 AI開発プラットフォーム',
                        'lavelo': '💾 プロンプト管理システム',
                        'rides': '🚗 データベース管理',
                        'files': '📁 ファイル管理',
                        'gradio': '🌐 HTML表示',
                        'rpa_automation': '🤖 RPA自動化システム',
                        'github_issue_dashboard': '🚀 GitHub ISSUE自動化',
                        'github_issue_automation': '🤖 GitHub ISSUE自動生成システム',
                        'integrated_approval_system': '🎯 統合承認システム',
                        'integrated_dashboard': '🚀 統合管理ダッシュボード',
                        'ui_verification_system': '🔧 UI検証・システム診断',
                    }
                    
                    # モジュールにtitle属性があるかチェック
                    if hasattr(module, 'interface_title'):
                        display_name = module.interface_title
                    elif base_name in title_mapping:
                        display_name = title_mapping[base_name]
                    else:
                        # デフォルトの美しいタイトル生成
                        formatted_name = base_name.replace('_', ' ').title()
                        display_name = f"✨ {formatted_name}"

                    # 名前の一意性を保証する処理
                    unique_name = display_name
                    count = 1

                    # 重複がある場合は番号を付与
                    while unique_name in gradio_interfaces:
                        unique_name = f"{display_name} ({count})"
                        count += 1

                    # Handle factory functions specifically
                    interface = module.gradio_interface
                    
                    # Check if it's a factory function by checking if it's callable but not a Gradio object
                    # Gradio objects have 'queue' method, regular functions don't
                    if callable(interface) and not hasattr(interface, 'queue'):
                        try:
                            interface = interface()
                        except Exception as call_error:
                            print(f"Failed to call factory function for {base_name}: {call_error}")
                            continue  # Skip this interface if factory function fails
                    
                    gradio_interfaces[unique_name] = interface
            except ModuleNotFoundError as e:
                print(f"ModuleNotFoundError: {sub_module_name} - {e}")
            except AttributeError as e:
                print(f"AttributeError in {sub_module_name}: {e}")
            except Exception as e:
                print(f"Failed to import {sub_module_name}: {e}")
                print(traceback.format_exc())

    # 名前とインターフェースのリストを返す
    print(f"Collected Gradio Interfaces: {list(gradio_interfaces.keys())}")
    return list(gradio_interfaces.values()), list(gradio_interfaces.keys())


def categorize_interfaces(interfaces, names):
    """インターフェースをカテゴリ別に分類"""
    categories = {
        "🚀 スタートガイド": [],
        "💬 チャット・会話": [],
        "🤖 AI・自動化": [],
        "📄 プロンプト・文書": [],
        "📊 管理・ダッシュボード": [],
        "🔧 開発・システム": [],
        "📁 データ・ファイル": [],
        "🌐 その他・連携": []
    }
    
    # カテゴリマッピング
    category_mapping = {
        "🚀 初心者ガイド": "🚀 スタートガイド",
        "💬 会話履歴管理": "💬 チャット・会話",
        "💬 AIチャット": "💬 チャット・会話",
        "🎯 会話履歴統合デモ": "💬 チャット・会話",
        "🤖 AI インタープリター": "🤖 AI・自動化",
        "🤖 Open Interpreter": "🤖 AI・自動化",
        "🤖 RPA自動化システム": "🤖 AI・自動化",
        "🤖 GitHub ISSUE自動生成システム": "🤖 AI・自動化",
        "🚀 GitHub ISSUE自動化": "🤖 AI・自動化",
        "📄 ドキュメント生成": "📄 プロンプト・文書",
        "💾 プロンプト管理システム": "📄 プロンプト・文書",
        "📄 プログラム生成AI": "📄 プロンプト・文書",
        "🚀 統合管理ダッシュボード": "📊 管理・ダッシュボード",
        "🎯 統合承認システム": "📊 管理・ダッシュボード",
        "🎯 ContBK統合ダッシュボード": "📊 管理・ダッシュボード",
        "🚀 Dify環境管理": "📊 管理・ダッシュボード",
        "🔧 UI検証・システム診断": "🔧 開発・システム",
        "✨ Memory Restore": "🔧 開発・システム",
        "✨ Memory Restore New": "🔧 開発・システム",
        "📁 ファイル管理": "📁 データ・ファイル",
        "🚗 データベース管理": "📁 データ・ファイル",
        "🌐 HTML表示": "🌐 その他・連携",
        "🐙 GitHub Issue Creator": "🌐 その他・連携",
        "🌤️ 天気予報": "🌐 その他・連携",
        "🖼️ 画像からUI生成": "🌐 その他・連携",
        "🎨 フロントエンド生成": "🌐 その他・連携"
    }
    
    # インターフェースを分類
    for interface, name in zip(interfaces, names):
        category = category_mapping.get(name, "🌐 その他・連携")
        categories[category].append((interface, name))
    
    return categories

def create_hierarchical_interface(categories):
    """階層化されたインターフェースを作成"""
    
    # まず、カテゴリごとに有効なインターフェースを収集
    valid_category_interfaces = []
    valid_category_names = []
    
    for category_name, category_interfaces in categories.items():
        if not category_interfaces:  # 空のカテゴリはスキップ
            continue
        
        try:
            if len(category_interfaces) == 1:
                # 1つの場合はそのまま使用
                interface, name = category_interfaces[0]
                valid_category_interfaces.append(interface)
                valid_category_names.append(f"{category_name}")
            else:
                # 複数の場合はサブタブを作成
                sub_interfaces = [item[0] for item in category_interfaces]
                sub_names = [item[1] for item in category_interfaces]
                
                # サブタブを作成
                sub_tabs = gr.TabbedInterface(sub_interfaces, sub_names)
                valid_category_interfaces.append(sub_tabs)
                valid_category_names.append(f"{category_name}")
                
        except Exception as e:
            print(f"カテゴリ {category_name} の処理でエラー: {e}")
            continue
    
    # メインのタブ付きインターフェースを作成
    if valid_category_interfaces:
        try:
            main_interface = gr.TabbedInterface(
                valid_category_interfaces, 
                valid_category_names,
                title="🚀 AI-Human協働開発システム"
            )
            return main_interface
        except Exception as e:
            print(f"メインインターフェース作成エラー: {e}")
            # フォールバック: シンプルなBlocks形式
            with gr.Blocks(title="🚀 AI-Human協働開発システム") as fallback_interface:
                gr.Markdown("# 🚀 AI-Human協働開発システム")
                gr.Markdown("**階層化インターフェースの作成に失敗しました。シンプル表示モードで動作しています。**")
                
                for i, (interface, name) in enumerate(zip(valid_category_interfaces, valid_category_names)):
                    with gr.Tab(name):
                        try:
                            interface.render()
                        except:
                            gr.Markdown(f"**{name}** の読み込みに失敗しました。")
            return fallback_interface
    else:
        # 有効なインターフェースがない場合
        with gr.Blocks(title="🚀 AI-Human協働開発システム") as empty_interface:
            gr.Markdown("# 🚀 システムが起動中です...")
            gr.Markdown("利用可能なインターフェースがありません。")
        return empty_interface

def setup_gradio_interfaces():
    """階層化されたGradioインターフェースを設定 - シンプル版"""
    print("🔍 setup_gradio_interfaces() 開始 - シンプル階層化")
    
    try:
        # インターフェースを取得
        gradio_interfaces, gradio_names = include_gradio_interfaces()
        print(f"🔍 取得したインターフェース数: {len(gradio_interfaces)}")
        
        if not gradio_interfaces:
            print("⚠️ インターフェースが見つかりません")
            with gr.Blocks(title="🚀 AI-Human協働開発システム") as minimal_interface:
                gr.Markdown("# 🚀 システムが起動中です...")
                gr.Markdown("利用可能なインターフェースがありません。")
            return minimal_interface
        
        # カテゴリ別に整理（シンプル版）
        startup_interfaces = []
        startup_names = []
        main_interfaces = []
        main_names = []
        
        for interface, name in zip(gradio_interfaces, gradio_names):
            if "初心者" in name or "ガイド" in name or "スタート" in name:
                startup_interfaces.append(interface)
                startup_names.append(name)
            else:
                main_interfaces.append(interface)
                main_names.append(name)
        
        # 階層化されたインターフェースを作成（シンプル版）
        print("🔍 シンプル階層化インターフェース作成")
        
        with gr.Blocks(title="🚀 AI-Human協働開発システム") as main_interface:
            gr.Markdown("# 🚀 AI-Human協働開発システム")
            gr.Markdown("**24時間での高速開発を実現する、genuineなAI-Human協働システム**")
            
            # スタートガイド
            if startup_interfaces:
                with gr.Tab("🚀 スタートガイド"):
                    gr.Markdown("### 初心者向けガイドと使い方")
                    if len(startup_interfaces) == 1:
                        startup_interfaces[0].render()
                    else:
                        startup_tabs = gr.TabbedInterface(startup_interfaces, startup_names)
            
            # その他の機能（最大10個まで）
            display_interfaces = main_interfaces[:10]
            display_names = main_names[:10]
            
            if display_interfaces:
                with gr.Tab("🛠️ システム機能"):
                    gr.Markdown(f"### システムの主要機能 ({len(display_interfaces)}個)")
                    if len(display_interfaces) == 1:
                        display_interfaces[0].render()
                    else:
                        main_tabs = gr.TabbedInterface(display_interfaces, display_names)
            
            # 残りの機能（もしあれば）
            if len(main_interfaces) > 10:
                remaining_interfaces = main_interfaces[10:]
                remaining_names = main_names[10:]
                with gr.Tab("� 追加機能"):
                    gr.Markdown(f"### その他の機能 ({len(remaining_interfaces)}個)")
                    if len(remaining_interfaces) == 1:
                        remaining_interfaces[0].render()
                    else:
                        remaining_tabs = gr.TabbedInterface(remaining_interfaces, remaining_names)
        
        print("✅ シンプル階層化インターフェース作成完了")
        main_interface.queue()
        return main_interface
        
    except Exception as e:
        print(f"❌ シンプル階層化でもエラー: {e}")
        import traceback
        traceback.print_exc()
        
        # 最終フォールバック: 従来のフラット形式
        print("🔄 従来形式にフォールバック")
        try:
            gradio_interfaces, gradio_names = include_gradio_interfaces()
            if gradio_interfaces:
                # 最大8個に制限
                safe_interfaces = gradio_interfaces[:8]
                safe_names = gradio_names[:8]
                print(f"🔍 フォールバック表示: {safe_names}")
                tabs = gr.TabbedInterface(safe_interfaces, safe_names, title="🚀 AI-Human協働開発システム")
                tabs.queue()
                return tabs
        except Exception as final_error:
            print(f"❌ 最終フォールバックもエラー: {final_error}")
            
        # 緊急フォールバック
        with gr.Blocks(title="🚀 AI-Human協働開発システム") as emergency_interface:
            gr.Markdown("# 🚀 システムが起動中です...")
            gr.Markdown("インターフェースの読み込みでエラーが発生しました。ページを再読み込みしてください。")
        return emergency_interface
if __name__ == "__main__":
    interfaces, names = include_gradio_interfaces()