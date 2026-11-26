# VirusTotal API Setup

This will be used to give the LLM some external security information about the URLs that are featured within the email that it has been given. This is designed to help with decision making with real data compared to the LLM judging it itself.

## 1. Create a VirusTotal Account

Navigate to:

https://www.virustotal.com

Create a free account.

---

## 2. Log Into VirusTotal

After logging in:

1. Click your profile icon.
2. Select **API Key**.

Alternatively, navigate to:

https://www.virustotal.com/gui/my-apikey

---

## 3. Copy Your API Key

Copy the API key that you are given and paste it into the .env file that you have created (information about the .env file in the README.md file).

.env file:
```python
VIRUSTOTAL_API_KEY = "{your API Key}"
```

---


## Usage Notes

The free API tier is limited to:

```text
4 requests per minute
500 requests per day
```
