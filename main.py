from config.gmail.get_gmail import get_gmail_service, get_message_text, get_unread_messages, mark_as_phishing, get_or_create_label, mark_as_read
from config.telegram_ollama_bot.telegram_bot import get_bot_prompt, get_user_prompt, get_bot_response, send_telegram_message

def get_gmail_data():
    service = get_gmail_service()
    unread_messages = get_unread_messages(service)
    phishing_label_id = get_or_create_label(service, "Phishing")
    
    return service, unread_messages, phishing_label_id

# RUN PROGRAM
gmail_data = get_gmail_data()

if not gmail_data[1]: # If there are no unread emails
    quit()
else:
    # Loop through each email
    for msg in gmail_data[1]:
        email = get_message_text(gmail_data[0], msg["id"])
        userPrompt = get_user_prompt(email)
        botPrompt = get_bot_prompt(userPrompt)
        response_data = get_bot_response(botPrompt)
        if response_data[0]["decision"] == "Phishing Email":
            send_telegram_message(response_data[1], gmail_data[0], gmail_data[2], msg["id"])
            mark_as_read(gmail_data[0], msg["id"])
            mark_as_phishing(gmail_data[0], msg["id"], gmail_data[2])
        quit()