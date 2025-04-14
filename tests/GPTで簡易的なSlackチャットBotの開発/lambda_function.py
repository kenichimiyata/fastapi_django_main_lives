import os
import json
from slack import WebClient, Msg
from transformers import pipeline

# Load environment variables
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']

# Initialize Slack client
client = WebClient(token=SLACK_BOT_TOKEN)

# Initialize ChatGPT model
chat_gpt = pipeline('conversational_ai', model='facebook/bart-base')

def lambda_handler(event, context):
    # Parse Slack event
    event_text = event['event']['text']
    user_id = event['event']['user']

    # Generate response using ChatGPT
    response = chat_gpt(event_text, max_length=100)

    # Post response to Slack channel
    client.chat_postMessage(
        channel=SLACK_CHANNEL,
        text=response
    )

    return {
        'statusCode': 200,
        'statusMessage': 'OK'
    }