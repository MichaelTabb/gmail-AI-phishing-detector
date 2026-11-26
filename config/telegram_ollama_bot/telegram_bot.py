import requests # Used to interact with the Ollama REST API
import json # Used to format JSON output
from dotenv import load_dotenv
import os

load_dotenv()

# Get the user prompt for the AI model
def get_user_prompt(email):
    userPrompt = f"""
    You are a cybersecurity expert who specialises in phishing detection within emails.

    Your task is to analyse the email provided below. The email may include text, headers, URLs, attachments, or metadata. Use whatever information is present.

    Follow these rules exactly:

    1. You will format your answer as:
    From: [The sender email address]
    Subject: [The subject line of the email]
    Decision: [Either "Phishing" or "Not Phishing]
    Reasoning: [3-4 sentences on your reasoning about your decision]

    For your reasoning, consider factors such as:
    - sender identity and domain
    - tone, urgency, or manipulation
    - suspicious links or attachments
    - header inconsistencies
    - impersonation attempts
    - unusual requests

    3. If some information is missing (e.g., no headers or no URLs), mention that in your reasoning but still make a determination.

    4. All of the links within the email are scanned externally. Use these scan results to help your reasoning.

    Here is the email to analyse:
    {email}
    """
    
    return userPrompt

# Get the bot prompt for the AI model
def get_bot_prompt(userPrompt):
    botPrompt = {
        "model": "mistral:latest",
        "prompt": userPrompt,
        "stream": False, # Makes it a single object instead of streams of objects
        "format": {
            "type": "object",
            "properties": { # What the AI model should return
                "from": {"type": "string"},
                "subject": {"type": "string"},
                "decision": {"type": "string"},
                "reasoning": {"type": "string"},
            },
        "required": ["from", "subject", "decision", "reasoning"]
        }
    }
    
    return botPrompt

# Get the bot response from the AI model
def get_bot_response(botPrompt):
    ollama_url = os.getenv("OLLAMA_URL")
    response = requests.post(ollama_url, json=botPrompt)
    outer = response.json()
    inner = outer["response"]
    clean_data = json.loads(inner)
    formatted_data = "From: " + clean_data["from"] + "\nSubject: " + clean_data["subject"] + "\n\nDecision: " + clean_data["decision"] + "\n\nReasoning: " + clean_data["reasoning"]
    print(formatted_data)
    return clean_data, formatted_data

# Send a Telegram message if the email is classified as a phishing email
def send_telegram_message(formatted_data, service, phishing_label_id, msg_id):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={formatted_data}"
    print(requests.get(url).json()) # this sends the message
