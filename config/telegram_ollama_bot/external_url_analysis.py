from dotenv import load_dotenv
import os
import requests

load_dotenv()

def VirusTotal_scan(url):
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

    return malicious, suspicious, harmless