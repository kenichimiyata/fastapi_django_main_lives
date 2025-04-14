import os
import shutil
import hmac
import hashlib
import base64
import subprocess
import time
from mysite.logger import logger
import async_timeout
import asyncio
import mysite.interpreter.interpreter_config 
from fastapi import HTTPException
from groq import Groq


GENERATION_TIMEOUT_SEC=60

def set_environment_variables():
    os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
    os.environ["OPENAI_API_KEY"] = os.getenv("api_key")
    os.environ["MODEL_NAME"] = "llama3-8b-8192"
    os.environ["LOCAL_MODEL"] = "true"

# Set the environment variable.
def chat_with_interpreter(
    message, history=None, a=None, b=None, c=None, d=None
):  # , openai_api_key):
    # Set the API key for the interpreter
    # interpreter.llm.api_key = openai_api_key
    if message == "reset":
        interpreter.reset()
        return "Interpreter reset", history
    full_response = ""
    # add_conversation(history,20)
    user_entry = {"role": "user", "type": "message", "content": message}
    #messages.append(user_entry)
    # Call interpreter.chat and capture the result
    messages = []
    recent_messages = history[-20:]
    for conversation in recent_messages:
        user_message = conversation[0]
        user_entry = {"role": "user", "content": user_message}
        messages.append(user_entry)
        assistant_message = conversation[1]
        assistant_entry = {"role": "assistant", "content": assistant_message}
        messages.append(assistant_entry)

    user_entry = {"role": "user", "content": message}
    messages.append(user_entry)
    #system_prompt = {"role": "system", "content": "あなたは日本語の優秀なアシスタントです。"}
    #messages.insert(0, system_prompt)

    for chunk in interpreter.chat(messages, display=False, stream=True):
        # print(chunk)
        # output = '\n'.join(item['content'] for item in result if 'content' in item)
        full_response = format_response(chunk, full_response)
        yield full_response  # chunk.get("content", "")

    yield full_response + rows  # , history
    return full_response, history

GENERATION_TIMEOUT_SEC = 60

def completion(message: str, history, c=None, d=None, prompt="あなたは日本語の優秀なアシスタントです。"):
    client = Groq(api_key=os.getenv("api_key"))
    messages = []
    recent_messages = history[-20:]
    for conversation in recent_messages:
        user_message = conversation[0]
        user_entry = {"role": "user", "content": user_message}
        messages.append(user_entry)
        assistant_message = conversation[1]
        assistant_entry = {"role": "assistant", "content": assistant_message}
        messages.append(assistant_entry)

    user_entry = {"role": "user", "content": message}
    messages.append(user_entry)
    system_prompt = {"role": "system", "content": prompt}
    messages.insert(0, system_prompt)

    #async with async_timeout.timeout(GENERATION_TIMEOUT_SEC):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        all_result = ""
        for chunk in response:
            current_content = chunk.choices[0].delta.content or ""
            all_result += current_content
            yield current_content
        yield all_result
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Stream timed out")
    except StopAsyncIteration:
        return

# 例としての使用方法
if __name__ == "__main__":
    history = [
        ("user message 1", "assistant response 1"),
        ("user message 2", "assistant response 2"),
    ]

    async def main():
        async for response in completion("新しいメッセージ", history):
            print(response)

    asyncio.run(main())