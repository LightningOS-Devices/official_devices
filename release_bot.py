import os
import requests
import json

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

ROM_NAME = "Lighting OS"
VERSION = os.getenv("VERSION")
DEVICE = os.getenv("DEVICE")
BUILD_DATE = os.getenv("BUILD_DATE")
MAINTAINER = os.getenv("MAINTAINER")
DOWNLOAD_URL = os.getenv("DOWNLOAD_URL")
CHANGELOG_URL = os.getenv("CHANGELOG_URL")
SUPPORT_URL = os.getenv("SUPPORT_URL")
FORUM_URL = os.getenv("FORUM_URL")
GUIDE_URL = os.getenv("GUIDE_URL")
MD5 = os.getenv("MD5")

def send_release_post():
    # 1. Format the main release text matching your design
    message = f"""
 **Official Lighting OS v{VERSION} Release!** 

 Codename: `{DEVICE}`
 Lighting OS version: `{VERSION}`
 Build date: `{BUILD_DATE}`
 MD5: `{MD5}`
 Maintainer: `{MAINTAINER}`
    """
    
    # 2. Build the interactive button grid layout
    keyboard = {
        "inline_keyboard": [
            [
                {"text": " Download", "url": DOWNLOAD_URL}
            ],
            [
                {"text": " Changelog", "url": CHANGELOG_URL},
                {"text": " Telegram Support", "url": SUPPORT_URL}
            ],
            [
                {"text": " XDA Forum", "url": FORUM_URL},
                {"text": " How to install/update", "url": GUIDE_URL}
            ]
        ]
    }
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message.strip(),
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
        "reply_markup": json.dumps(keyboard)
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Successfully posted stylized release to channel!")
    else:
        print(f"Failed to post: {response.text}")

if __name__ == "__main__":
    send_release_post()
