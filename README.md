# Gmail Phishing Detector

An AI-powered phishing detection system that monitors unread Gmail messages, analyzes them using a local Large Language Model (LLM), and sends suspicious emails to Telegram for human review before taking action.

## Features

- Retrieves unread emails from Gmail
- Uses a local LLM (Ollama) to classify emails
- Sends analysis results to Telegram is classified as phishing
- Automatically files confirmed phishing emails
- Runs locally for enhanced privacy
- Fully configurable through environment variables

## How It Works

1. Retrieve unread emails from Gmail.
2. Extract the email content.
3. Send the content to the LLM for analysis.
4. Receive:
   - Sender of the email
   - Subject of the email
   - Classification (Phishing / Legitimate)
   - Explanation
5. Send the result to Telegram when classified as phishing.
6. Email is moved to the appropriate folder based on the response.

## Architecture

```text
Gmail
  │
  ▼
Unread Emails
  │
  ▼
Phishing Detector
  │
  ▼
Ollama LLM
  │
  ▼
Classification Result
  │
  ▼
Telegram Notification
  │
  ▼
User Approval
  │
  ▼
Move Email to Folder
```

## Tech Stack

- Python
- Gmail API
- Ollama
- Telegram Bot API
- JSON
- OAuth 2.0

## Installation

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/gmail-phishing-detector.git
cd gmail-phishing-detector
```

### Create a virtual environment

```bash
python -m venv venv
```

Activate it:

Windows:

```bash
venv\Scripts\activate
```

Linux / Raspberry Pi:

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN = 
TELEGRAM_CHAT_ID = 
OLLAMA_URL = 
```

Never upload the `.env` file to GitHub.

## Running the Application

```bash
python main.py
```

## Project Structure

```text
gmail-phishing-detector/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
├── gmail/
├── classification/
├── telegram/
├── config/
├── logs/
└── credentials/
```

## Example Output

```text
From: John Doe
Subject: Test Email
Classification: Phishing
Reason: The email contains urgency language, suspicious links,
and requests credential verification.
```

## Security

- API keys are stored in environment variables.
- Sensitive files are excluded using `.gitignore`.
- Gmail authentication uses OAuth 2.0.

## Future Improvements

- Human-in-the-loop approving
- Attachment scanning
- URL reputation checking
- Email sender reputation analysis
- Statistics and reporting
- Machine learning feedback loop

## License

This project is for educational and personal use.

## Author

Michael Tabbinor