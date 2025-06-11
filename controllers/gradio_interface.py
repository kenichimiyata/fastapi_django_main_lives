import gradio as gr
from llamafactory.webui.interface import create_ui

def create_gradio_interface():
    """Gradio インターフェースを作成する"""
    return create_ui()

# Gradio インターフェースを作成
with gr.Blocks() as gradio_interface:
    # LlamaFactory UIを追加
    llamafactory_demo = create_gradio_interface()
    
    # LlamaFactory UIを現在のBlocksに統合
    with gr.Row():
        with gr.Column():
            gr.HTML("""
            <h2>🦙 LlamaFactory WebUI</h2>
            <p>LlamaFactoryのWebUIインターフェースです</p>
            """)
    
    # LlamaFactory UIをマウント
    llamafactory_demo.render()
