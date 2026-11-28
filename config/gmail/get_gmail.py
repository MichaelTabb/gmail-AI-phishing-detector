# Google libraries to allow for gmail API to work
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config.telegram_ollama_bot.external_url_analysis import Google_scan, VirusTotal_scan
import base64
import re

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

# Connect to gmail api
def get_gmail_service():
    creds = None
    
    # First time loging to create token.json
    try:
        creds = Credentials.from_authorized_user_file("config/credentials/token.json", SCOPES)
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

    url_list = get_urls(body)

    # Get the malicious URLs from the URL list and scan them via VirusTotal
    malicious_urls = []
    for result in url_list:
        if result["status"] == "MALICIOUS":
            malicious_urls.append(result["url"])

    malicious_url_results = VirusTotal_scan(malicious_urls)

    cleaned_email = clean_email(body)

    # Combine the email aspects together
    email = {
        "From": sender,
        "To": to,
        "Date": date,
        "Message ID": message_id,
        "Subject": subject,
        "Body": cleaned_email,
        "Google Safe Search Results": url_list,
        "VirusTotal Results": malicious_url_results
    }
    
    return email

def clean_email(email):
    clean = re.compile('<.*?>')
    cleanEmail = re.sub(clean, '', email)
    cleanEmail = cleanEmail.replace("\n", "")
    cleanEmail = cleanEmail.replace("\r", "")
    
    return cleanEmail

# Search the email body for URLs
def get_urls(email_body):
    # Pattern used to get URLs from plaintext or from HTML tags
    pattern = (
        r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        r'(?:/[^\s<>"\']*)?'
    )

    # Find all of the URLs in the body of the email
    urls = re.findall(pattern, email_body)
    # Used to hold all of the URLs and their results
    url_results = []

    # Add every URL and its scan result to the list
    for url in urls:
        url_scan = Google_scan(url)
        url_results.append(url_scan)

    return url_results

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