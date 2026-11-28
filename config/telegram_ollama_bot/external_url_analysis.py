from dotenv import load_dotenv
import os
import requests

load_dotenv()

def Google_scan(url):
    googleAPI = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY")

    endpoint = (
        f"https://safebrowsing.googleapis.com/v4/threatMatches:find"
        f"?key={googleAPI}"
    )

    payload = {
        "client": {
            "clientId": "gmail-ai-phishing-detector",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE"
            ],
            "platformTypes": [
                "ANY_PLATFORM"
            ],
            "threatEntryTypes": [
                "URL"
            ],
            "threatEntries": [
                {
                    "url": url
                }
            ]
        }
    }

    response = requests.post(
        endpoint,
        json=payload
    )

    data = response.json()

    # Return if the URL is safe
    if "matches" not in data:
        return {
            "url": url,
            "status": "SAFE",
            "threat_type": None
        }

    # Return if the URL is Malicious
    return {
        "url": url,
        "status": "MALICIOUS",
        "threat_type": data["matches"][0]["threatType"]
    }

def VirusTotal_scan(urls):
    data = {}

    for url in urls:
        headers = {
            "x-apikey": os.getenv("VIRUSTOTAL_API_KEY")
        }

        response = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data={
                "url": url
            }
        )

        analysis_id = response.json()["data"]["id"]

        response = requests.get(
            f"https://www.virustotal.com/api/v3/analyses/{analysis_id}",
            headers=headers
        )

        stats = response.json()["data"]["attributes"]["stats"]

        malicious = stats["malicious"]
        suspicious = stats["suspicious"]
        harmless = stats["harmless"]

        data[url] = [f"Malicious: {malicious}, Suspicious: {suspicious}, Harmless: {harmless}"]

    return data