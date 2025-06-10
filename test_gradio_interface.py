#!/usr/bin/env python3
"""
Test Gradio interface for OpenInterpreter directly
"""

import os
import sys
import django
from django.conf import settings

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# Add the project directory to Python path
sys.path.append('/workspaces/fastapi_django_main_live')

# Configure Django
django.setup()

import gradio as gr
from controllers.gra_02_openInterpreter.OpenInterpreter import chat_with_interpreter, add_message_to_db, get_recent_messages

def create_gradio_interface():
    """Create a simple Gradio interface for OpenInterpreter"""
    
    def chat_interface(message, password, history):
        """Wrapper for chat_with_interpreter that works with Gradio"""
        if not message.strip():
            return history, ""
        
        # Get the response from chat_with_interpreter - note the password parameter name is 'passw'
        responses = []
        for response in chat_with_interpreter(message, history, passw=password):
            responses.append(response)
        
        # Combine all responses
        full_response = "".join(responses) if responses else "No response generated"
        
        # Add to history
        history.append([message, full_response])
        
        return history, ""
    
    def get_chat_history():
        """Get recent chat history from database"""
        try:
            messages = get_recent_messages(10)
            history = []
            for msg in messages:
                if msg[0] == 'user':  # role is the first element
                    user_msg = msg[2]  # content is the third element
                    # Find the corresponding assistant response
                    for response_msg in messages:
                        if (response_msg[0] == 'assistant' and 
                            messages.index(response_msg) > messages.index(msg)):
                            history.append([user_msg, response_msg[2]])
                            break
            return history
        except Exception as e:
            print(f"Error getting chat history: {e}")
            return []
    
    # Create the interface
    with gr.Blocks(title="OpenInterpreter Test") as demo:
        gr.Markdown("# OpenInterpreter Chat Interface")
        gr.Markdown("Password: 12345")
        
        chatbot = gr.Chatbot(
            value=get_chat_history(),
            height=400,
            show_label=False,
            avatar_images=(None, None)
        )
        
        with gr.Row():
            with gr.Column(scale=4):
                message_input = gr.Textbox(
                    placeholder="Enter your message here...",
                    show_label=False,
                    container=False
                )
            with gr.Column(scale=1):
                password_input = gr.Textbox(
                    value="12345",
                    placeholder="Password",
                    type="password",
                    show_label=False
                )
        
        send_button = gr.Button("Send", variant="primary")
        clear_button = gr.Button("Clear History")
        
        # Event handlers
        send_button.click(
            chat_interface,
            inputs=[message_input, password_input, chatbot],
            outputs=[chatbot, message_input]
        )
        
        message_input.submit(
            chat_interface,
            inputs=[message_input, password_input, chatbot],
            outputs=[chatbot, message_input]
        )
        
        clear_button.click(
            lambda: ([], ""),
            outputs=[chatbot, message_input]
        )
    
    return demo

if __name__ == "__main__":
    print("Creating Gradio interface...")
    demo = create_gradio_interface()
    print("Starting Gradio server...")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7862,
        share=False,
        debug=True
    )
