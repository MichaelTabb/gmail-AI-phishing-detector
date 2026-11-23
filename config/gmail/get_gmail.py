from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
import re

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

# Connect to gmail api
def get_gmail_service():
    creds = None
    
    # First time loging to create token.json
    try:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    except:
        flow = InstalledAppFlow.from_client_secrets_file("config/credentials/credentials.json", SCOPES)
        creds = flow.run_local_server(port=0, access_type = 'offline', prompt = 'consent')
        with open("config/credentials/token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

# Get all of the unread emails
def get_unread_messages(service):
    results = service.users().messages().list(
        userId = "me",
        q = "is:unread"
    ).execute()

    return results.get("messages", [])

# Get the headers and body of the email
def get_message_text(service, msg_id):
    msg = service.users().messages().get(
        userId = "me",
        id = msg_id,
        format = "full"
    ).execute()
    
    headers = msg["payload"]["headers"]
    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
    body = ""
    
    def get_header(name):
        for h in headers:
            if h["name"].lower() == name.lower():
                return h["value"]
        return ""
    
    sender = get_header("From")
    to = get_header("To")
    date = get_header("Date")
    message_id = get_header("Message-ID")
    
    if "parts" in msg["payload"]:
        for part in msg["payload"]["parts"]:
            if part["mimeType"] == "text/plain":
                body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                break
    else:
        if msg["payload"]["mimeType"] == "text/plain":
            body = base64.urlsafe_b64decode(msg["payload"]["data"]).decode("utf-8")
    
    email = {
        "From": sender,
        "To": to,
        "Date": date,
        "Message ID": message_id,
        "Subject": subject,
        "Body": body
    }
    
    cleaned_email = clean_email(email['Body'])
    
    return cleaned_email

def clean_email(email):
    clean = re.compile('<.*?>')
    cleanEmail = re.sub(clean, '', email)
    cleanEmail = cleanEmail.replace("\n", "")
    cleanEmail = cleanEmail.replace("\r", "")
    
    return cleanEmail

# Get / create the phishing label
def get_or_create_label(service, label_name):
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    
    for label in labels:
        if label["name"].lower() == label_name.lower():
            return label["id"]
    
    label_body = {
        "name": label_name,
        "labelListVisibility": "labelShow",
        "messagelistVisibility": "show"
    }
    
    new_label = service.users().create(
        userId="me",
        body = label_body
    ).execute()
    
    return new_label

# Send a phishing email to the label folder
def mark_as_phishing(service, msg_id, phishing_label_id):
    service.users().messages().modify(
        userId = "me",
        id = msg_id,
        body = {
            "addLabelIds": [phishing_label_id],
            "removelabelIds": ["INBOX"]
        }
    ).execute()

def mark_as_read(service, msg_id):
    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={
            "removeLabelIds": ["UNREAD"]
        }
    ).execute()