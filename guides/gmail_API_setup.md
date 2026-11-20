# Gmail API Configuration

To give your AI model access to your gmail, you need to create a google cloud project, enable and configure the gmail API.

## 1. Create Google Cloud Project

Before configuring the gmail API, you first need to create a Google Cloud Project.

Navigate to:

https://console.cloud.google.com

and create a new project.

---

## 2. Enable Gmail API

Now that the Google Cloud project is created, you can now setup the gmail API.

Navigate to:

APIs & Services

↓

Library

↓

Search for:

Gmail API

↓

Enable

---

## 3. Configure OAuth Consent Screen

Now it's time to configure the authentication for the API.

Navigate to:

APIs & Services

↓

OAuth Consent Screen

Choose:

External

Add:

- App Name
- Email Address

Save.

---

## 4. Add Test User

For personal use, add yourself as a test user.

Navigate:

OAuth Consent Screen

↓

Test Users

Add your Gmail address.

Example:

yourname@gmail.com

---

## 5. Create OAuth Credentials

Now you need to configure and create the credentials for the authentication.

Navigate:

Credentials

↓

Create Credentials

↓

OAuth Client ID

Select:

Desktop Application

Name:

PhishingFilter

---

## 6. Download Credentials

Now you need a credentials file so that you can use the gmail API.

Download:

credentials.json

Place inside your project folder.

Example:

```text
phishing-filter/
├── credentials.json
├── main.py
├── venv/
```

---

## 7. Create Virtual Environment

For the program to work correctly, you'll need to create and activate a virtual environment.

### Linux

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
```

Activate:

```powershell
venv\Scripts\activate
```

---

## 8. First Authentication

Once you have configured the authentication and configured the program, you need to run it the first time to authenticate the project.

**NOTE:** If you change the scope of the get_gmail.py file, you will have too re-authenticate the program to work again.

### Linux

```bash
python3 main.py
```

### Windows

```powershell
python main.py
```

A browser window will open.

Sign into Gmail.

Approve permissions.

Google will generate:

```text
credentials.json
```

In the project directory, create a folder called "credentials" and move the "credentials.json" file into it.
