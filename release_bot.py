import os
import requests
import json
import re
from io import BytesIO

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
BANNER_IMAGE_URL = os.getenv("BANNER_IMAGE_URL")

ROM_NAME = "Lighting OS"
VERSION = os.getenv("VERSION")
DEVICE = os.getenv("DEVICE")
BUILD_DATE = os.getenv("BUILD_DATE")
MAINTAINER = os.getenv("MAINTAINER")
MD5 = os.getenv("MD5")
BUILD_TYPE = os.getenv("BUILD_TYPE", "GAPPS")

def clean_url(url_string):
    if not url_string:
        return ""
    match = re.search(r'https?://[^\s()]+', url_string)
    if match:
        return match.group(0)
    return url_string.strip().strip("'\"<>[]()")

DOWNLOAD_URL = clean_url(os.getenv("DOWNLOAD_URL"))
CHANGELOG_URL = clean_url(os.getenv("CHANGELOG_URL"))
ROM_CHANGELOG = clean_url(os.getenv("ROM_CHANGELOG"))
DEVICE_CHANGELOG = clean_url(os.getenv("DEVICE_CHANGELOG"))
SUPPORT_URL = clean_url(os.getenv("SUPPORT_URL"))
GUIDE_URL = clean_url(os.getenv("GUIDE_URL"))

def send_release_post():
    rom_cl_text = f"\n📦 **ROM Changelog:** {ROM_CHANGELOG}" if ROM_CHANGELOG else ""
    device_cl_text = f"\n📱 **Device Changelog:** {DEVICE_CHANGELOG}" if DEVICE_CHANGELOG else ""

    caption = f"""
⚡ **Official Lighting OS v{VERSION} ({BUILD_TYPE}) Release!** ⚡

🏷 **Codename:** `{DEVICE}`
🤖 **Lighting OS version:** `{VERSION}`
📦 **Variant:** `{BUILD_TYPE}`
📅 **Build date:** `{BUILD_DATE}`
✅ **MD5:** `{MD5}`
🧑‍💻 **Maintainer:** `{MAINTAINER}`{rom_cl_text}{device_cl_text}
    """
    
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
                {"text": "❓ Guide", "url": GUIDE_URL}
            ]
        ]
    }
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHANNEL_ID,
        "caption": caption.strip(),
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
        "reply_markup": json.dumps(keyboard)
    }
    
    if BANNER_IMAGE_URL:
        try:
            response = requests.get(BANNER_IMAGE_URL)
            if response.status_code == 200:
                files = {'photo': ('banner.png', BytesIO(response.content))}
                response = requests.post(url, data=payload, files=files)
                if response.status_code == 200:
                    print("Successfully posted release with banner!")
                    return
            print("Banner send failed or URL invalid, falling back to text.")
        except Exception as e:
            print(f"Error: {e}")
            
    fallback_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload["text"] = payload.pop("caption")
    requests.post(fallback_url, json=payload)

if __name__ == "__main__":
    send_release_post()
