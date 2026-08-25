import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

ROM_NAME = "Lighting OS"
VERSION = os.getenv("VERSION")
DEVICE = os.getenv("DEVICE")
MAINTAINER = os.getenv("MAINTAINER")
DOWNLOAD_URL = os.getenv("DOWNLOAD_URL")
MD5 = os.getenv("MD5")
CHANGELOG = os.getenv("CHANGELOG")

def send_release_post():
    message = f"""
⚡ **{ROM_NAME} {VERSION} Official Release!** ⚡

📱 **Device:** `{DEVICE}`
👤 **Maintainer:** {MAINTAINER}

🛠 **Changelog:**
{CHANGELOG}

📥 **Download (Gofile):**
[Get Build Here]({DOWNLOAD_URL})

🔑 **MD5:** `{MD5}`
    """
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message.strip(),
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Successfully posted maintainer build to channel!")
    else:
        print(f"Failed to post: {response.text}")

if __name__ == "__main__":
    send_release_post()
