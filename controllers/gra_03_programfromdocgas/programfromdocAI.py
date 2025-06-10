import gradio as gr
from mysite.libs.utilities import chat_with_interpreter, completion, process_file,no_process_file
from interpreter import interpreter
import mysite.interpreter.interpreter_config  # インポートするだけで設定が適用されます
import duckdb
import gradio as gr
import psycopg2
from dataclasses import dataclass, field
from typing import List, Optional
from mysite.interpreter.process import no_process_file,process_file
#from controllers.gra_04_database.rides import test_set_lide

val = """
# gradio で miiboのナレッジに登録する画面の作成
  gradio_interface interfacec name

# fastapi
  gradio apiに接続するAPI
  router で作成

1ファイルで作成
仕様書の作成
plantumlで図にする

#sample fastapi
import requests
import json
import os
# current_user: User = Depends(get_current_active_user)):
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
# current_user: User = Depends(get_current_active_user)):
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

from fastapi import APIRouter, HTTPException
from gradio_client import Client

#router = APIRouter()
router = APIRouter(prefix="/gradio", tags=["gradio"])
@router.get("/route/gradio")

def get_senario(id,res):
    table = "LOG"

    client = Client("kenken999/fastapi_django_main_live")
    result = client.predict(
            message="Hello!!",
            request=0.95,
            param_3=512,
            api_name="/chat"
    )
    return result



"""


gradio_interface = gr.Interface(
    fn=process_file,
    inputs=[
        "file",
        gr.Textbox(label="Additional Notes", lines=10, value=val),
        gr.Textbox(label="Folder Name", value="test_folders"),
        gr.Textbox(label="github token", value="***********************"),
    ],
    outputs="text"
)