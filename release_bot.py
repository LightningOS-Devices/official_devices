import os
import requests
import json
import re

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

ROM_NAME = "Lighting OS"
VERSION = os.getenv("VERSION")
DEVICE = os.getenv("DEVICE")
BUILD_DATE = os.getenv("BUILD_DATE")
MAINTAINER = os.getenv("MAINTAINER")
MD5 = os.getenv("MD5")

def clean_url(url_string):
    if not url_string:
        return ""
    match = re.search(r'https?://[^\s()]+', url_string)
    if match:
        return match.group(0)
    return url_string.strip().strip("'\"<>[]()")

DOWNLOAD_URL = clean_url(os.getenv("DOWNLOAD_URL"))
CHANGELOG_URL = clean_url(os.getenv("CHANGELOG_URL"))
SUPPORT_URL = clean_url(os.getenv("SUPPORT_URL"))
FORUM_URL = clean_url(os.getenv("FORUM_URL"))
GUIDE_URL = clean_url(os.getenv("GUIDE_URL"))

def send_release_post():
    message = f"""
⚡ **Official Lighting OS v{VERSION} Release!** ⚡

🏷 **Codename:** `{DEVICE}`
🤖 **Lighting OS version:** `{VERSION}`
📅 **Build date:** `{BUILD_DATE}`
✅ **MD5:** `{MD5}`
🧑‍💻 **Maintainer:** `{MAINTAINER}`
    """
    
    # Compact button layout configuration
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "📥 Download", "url": DOWNLOAD_URL}
            ],
            [
                {"text": "📝 Changelog", "url": CHANGELOG_URL},
                {"text": "⚡ Support", "url": SUPPORT_URL}
            ],
            [
                {"text": "🌐 XDA", "url": FORUM_URL},
                {"text": "❓ Guide", "url": GUIDE_URL}
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
