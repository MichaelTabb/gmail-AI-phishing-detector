# Google Safe Browsing API Setup

This will be used to give the LLM some external security information about the URLs that are featured within the email that it has been given. This is designed to help with decision making with real data compared to the LLM judging it itself.

## Prerequisites

* Gmail API Configured

## 1. Open Google Cloud Console

Navigate to:

https://console.cloud.google.com

You should automatically be on the project you created when setting up the Gmail API. If not, select your project.
---


## 2. Enable Safe Browsing API

Before creating the API key, you need to enable the Safe Browsing API as it is not enabled by default.

Navigate to:

```text
APIs & Services
```

↓

```text
Library
```

↓

Search:

```text
Safe Browsing API
```

↓

Click:

```text
Enable
```

---

## 3. Create API Key

After enabling the Safe Browsing API, you then need to create the API Key

Navigate to:

```text
APIs & Services
```

↓

```text
Credentials
```

↓

```text
Create Credentials
```

↓

```text
API Key
```

Enter the name of the API Key.

Under:

```text
Select API restrictions
```

Choose:

```text
Safe Browsing API
```

Then under:

```text
Application restrictions
```

Select:

```text
None
```

Click:

```text
Save
```

## 4. Copy the API Key

Copy the API key that you are given and paste it into the .env file that you have created (information about the .env file in the README.md file).

.env file:
```python
GOOGLE_SAFE_BROWSING_API_KEY = "{your API Key}"
```

---