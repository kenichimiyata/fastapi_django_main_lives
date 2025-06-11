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
    package_dir = "controllers"  # 相対パスでcontrollersディレクトリを指定
    gradio_interfaces = {}  # 辞書型: { interface_name: gradio_interface }
    
    # `controllers/` 以下の全てのサブディレクトリを探索
    package_paths = []
    for root, dirs, files in os.walk(package_dir):
        if "__pycache__" in root:  # `__pycache__` を除外
            continue
        package_paths.append(root)

    for package_path in package_paths:
        # パッケージの Python モジュールを取得
        rel_path = os.path.relpath(package_path, package_dir)
        package_name = "controllers" + (("." + rel_path.replace(os.sep, ".")) if rel_path != "." else "")

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
                        'contbk_example': '🎯 ContBK ダッシュボード',
                        'contbk_dashboard': '📊 ContBK 統合',
                        'conversation_history': '💬 会話履歴管理',
                        'conversation_logger': '📝 会話ログ',
                        'example_gradio_interface': '🔧 サンプル',
                        'hasura': '🗄️ Hasura API',
                        'Chat': '💬 チャット',
                        'OpenInterpreter': '🤖 AI インタープリター',
                        'programfromdoc': '📄 ドキュメント生成',
                        'gradio_interface': '🚀 AI開発',
                        'lavelo': '💾 プロンプト管理',
                        'rides': '🚗 データベース',
                        'files': '📁 ファイル管理',
                        'gradio': '🌐 HTML表示',
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

                    gradio_interfaces[unique_name] = module.gradio_interface
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

    tabs = gr.TabbedInterface(all_interfaces, all_names)
    tabs.queue()
    return tabs
if __name__ == "__main__":
    interfaces, names = include_gradio_interfaces()