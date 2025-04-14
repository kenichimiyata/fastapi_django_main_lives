import gradio as gr
import os
import shutil
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

if __name__ == "__main__":
    uvicorn.run("mysite.asgi:app", host="0.0.0.0", port=7860)
# uvicorn.run("mysite.asgi:app", host="0.0.0.0", port=7860, reload=True)
