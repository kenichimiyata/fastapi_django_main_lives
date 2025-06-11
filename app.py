import gradio as gr
import os
import shutil
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
import uvicorn
from groq import Groq

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Any, Coroutine, List

from starlette.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

from groq import AsyncGroq, AsyncStream, Groq
from groq.lib.chat_completion_chunk import ChatCompletionChunk
from groq.resources import Models
from groq.types import ModelList
from groq.types.chat.completion_create_params import Message

import async_timeout
import asyncio
from interpreter import interpreter
import os

GENERATION_TIMEOUT_SEC = 60
import os

from llamafactory.webui.interface import create_ui

# Gradio インターフェース作成
demo = create_ui()

if __name__ == "__main__":
    import sys
    
    # Hugging Face Spacesでの実行を検出
    if os.getenv("SPACE_ID") or "--gradio" in sys.argv:
        print("🤗 Hugging Face Spacesでアプリケーションを起動しています...")
        demo.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=True,
            show_error=True
        )
    else:
        # デバッグモードかどうかを判定
        is_debug = "--debug" in sys.argv or any("debugpy" in arg for arg in sys.argv)
    
    try:
        print("🚀 アプリケーションを開始しています...")
        
        if is_debug:
            print("🐛 デバッグモード: リロードを無効化してブレークポイントを有効にします")
            # デバッグモード: reloadを無効にしてブレークポイントを使用可能に
            uvicorn.run(
                "mysite.asgi:app", 
                host="0.0.0.0", 
                port=7860, 
                reload=False,  # デバッグ時はリロード無効
                log_level="debug",
                access_log=True,
                use_colors=True
            )
        else:
            print("📍 開発モード: ホットリロードが有効です")
            # 開発モード: reloadを有効にして高速開発
            uvicorn.run(
                "mysite.asgi:app", 
                host="0.0.0.0", 
                port=7860, 
                reload=True,  # 開発時はリロード有効
                log_level="debug",
                access_log=True,
                use_colors=True,
                reload_dirs=["/workspaces/fastapi_django_main_live"]
            )
            
    except Exception as e:
        print(f"❌ アプリケーション起動エラー: {e}")
        import traceback
        traceback.print_exc()
