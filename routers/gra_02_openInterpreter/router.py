from fastapi import APIRouter
from .OpenInterpreter import gradio_interface

router = APIRouter()

# You can add specific API endpoints here if needed
# For now, the Gradio interface will be mounted in the main application
