import os
import requests
import json
import re
from io import BytesIO

# --- Bot and Channel Setup ---
# Ensure these secrets are set in your GitHub repository settings
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

# --- Banner Configuration ---
# Host your finalized banner (image_15.png) on GitHub Pages, Imgur, etc.,
# and set the direct URL as this secret in your GitHub Actions
BANNER_IMAGE_URL = os.getenv("BANNER_IMAGE_URL")

# --- Release Data ---
# These are populated by the GitHub Actions workflow inputs
ROM_NAME = "Lighting OS"
VERSION = os.getenv("VERSION")
DEVICE = os.getenv("DEVICE")
BUILD_DATE = os.getenv("BUILD_DATE")
MAINTAINER = os.getenv("MAINTAINER")
MD5 = os.getenv("MD5")

# --- Helper Function ---
def clean_url(url_string):
    """Sanitizes URLs to prevent markdown formatting breaks in Telegram buttons."""
    if not url_string:
        return ""
    # Strip markdown format like [text](url) or stray brackets/quotes
    match = re.search(r'https?://[^\s()]+', url_string)
    if match:
        return match.group(0)
    return url_string.strip().strip("'\"<>[]()")

# --- Clean URLs ---
DOWNLOAD_URL = clean_url(os.getenv("DOWNLOAD_URL"))
CHANGELOG_URL = clean_url(os.getenv("CHANGELOG_URL"))
SUPPORT_URL = clean_url(os.getenv("SUPPORT_URL"))
FORUM_URL = clean_url(os.getenv("FORUM_URL"))
GUIDE_URL = clean_url(os.getenv("GUIDE_URL"))

# --- Main Function ---
def send_release_post():
    """Posts the release banner, caption, and compact buttons to Telegram."""
    
    # Format the release details as a caption
    caption = f"""
⚡ **Official Lighting OS v{VERSION} Release!** ⚡

🏷 **Codename:** `{DEVICE}`
🤖 **Lighting OS version:** `{VERSION}`
📅 **Build date:** `{BUILD_DATE}`
✅ **MD5:** `{MD5}`
🧑‍💻 **Maintainer:** `{MAINTAINER}`
    """
    
    # Define the compact 2-by-2 button grid
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
    
    # --- Telegram API Method: sendPhoto ---
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    
    # Prepare the base payload for sendPhoto
    payload = {
        "chat_id": CHANNEL_ID,
        "caption": caption.strip(),  # The release text is now a caption
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
        "reply_markup": json.dumps(keyboard)
    }
    
    # If a BANNER_IMAGE_URL is provided, download and send it
    if BANNER_IMAGE_URL:
        try:
            print(f"Downloading banner from: {BANNER_IMAGE_URL}...")
            response = requests.get(BANNER_IMAGE_URL)
            
            if response.status_code == 200:
                # Prepare the file for the multipart request
                files = {'photo': ('banner.png', BytesIO(response.content))}
                
                print("Posting release to Telegram with banner and buttons...")
                response = requests.post(url, data=payload, files=files)
                
                if response.status_code == 200:
                    print("Successfully posted stylized release with banner!")
                else:
                    print(f"Failed to post photo to Telegram: {response.status_code} - {response.text}")
                    # Fallback to sendMessage if sendPhoto fails (rare)
                    _fallback_send_message(BOT_TOKEN, CHANNEL_ID, caption.strip(), keyboard)
            else:
                print(f"Failed to download banner image. Status code: {response.status_code}")
                # Fallback to sendMessage if download fails
                _fallback_send_message(BOT_TOKEN, CHANNEL_ID, "⚠️ Banner image could not be loaded. " + caption.strip(), keyboard)
                
        except Exception as e:
            print(f"Error sending with banner: {e}")
            # General error fallback
            _fallback_send_message(BOT_TOKEN, CHANNEL_ID, "⚠️ An error occurred while processing the banner. " + caption.strip(), keyboard)
    else:
        print("No BANNER_IMAGE_URL provided in environment variables. Sending as text-only.")
        # Fallback to sendMessage if no URL is configured
        _fallback_send_message(BOT_TOKEN, CHANNEL_ID, caption.strip(), keyboard)

def _fallback_send_message(token, channel_id, text, keyboard):
    """Helper function to send as text-only if banner posting fails."""
    print("Attempting fallback sendMessage...")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": channel_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
        "reply_markup": json.dumps(keyboard)
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Fallback successful.")
    else:
        print(f"Fallback failed: {response.text}")

if __name__ == "__main__":
    send_release_post()
