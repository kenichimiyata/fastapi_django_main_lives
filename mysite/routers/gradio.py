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


def setup_gradio_interfaces():
    ##
    #from routers.gra_06_video.video import gradio_interface as video
    default_interfaces = []#,demo]
    default_names = ["CreateTASK","Chat","OpenInterpreter","DataBase","CreateFromDOC","HTML","FILES"]#"demo"]

    gradio_interfaces, gradio_names = include_gradio_interfaces()

    all_interfaces = gradio_interfaces
    all_names = gradio_names

    try:
        # Create a fresh TabbedInterface to avoid rendering conflicts
        tabs = gr.TabbedInterface(all_interfaces, all_names)
        tabs.queue()
        return tabs
    except Exception as e:
        print(f"❌ TabbedInterface creation failed: {e}")
        # Fallback: create a simple interface with more interfaces including integrated dashboard
        # Try to include at least 12 interfaces to capture the integrated dashboard (#11)
        safe_interfaces = all_interfaces[:12] if len(all_interfaces) > 12 else all_interfaces
        safe_names = all_names[:12] if len(all_names) > 12 else all_names
        
        if safe_interfaces:
            try:
                fallback_tabs = gr.TabbedInterface(safe_interfaces, safe_names)
                fallback_tabs.queue()
                return fallback_tabs
            except Exception as fallback_error:
                print(f"❌ Fallback interface creation failed: {fallback_error}")
                # Return a minimal working interface
                with gr.Blocks() as minimal_interface:
                    gr.Markdown("# 🚀 システムが起動中です...")
                    gr.Markdown("インターフェースの読み込みでエラーが発生しました。")
                return minimal_interface
        else:
            # Return a minimal working interface
            with gr.Blocks() as minimal_interface:
                gr.Markdown("# 🚀 システムが起動中です...")
                gr.Markdown("利用可能なインターフェースがありません。")
            return minimal_interface
if __name__ == "__main__":
    interfaces, names = include_gradio_interfaces()