# Lighting OS Release Guide

### How to push a build update:
1. Compile your build and upload the zip to your personal Gofile server.
2. Go to the **Actions** tab in this GitHub repository.
3. Select **Lighting OS Release Bot** on the left sidebar.
4. Click the **Run workflow** dropdown button.
5. Fill out the form fields:
   - **Device Codename:** (e.g., `redfin`)
   - **ROM Version:** (e.g., `v1.5`)
   - **Maintainer Name:** (Your Telegram handle)
   - **Gofile Download Link:** (Paste your link here)
   - **MD5 Checksum:** (Paste your MD5 hash)
   - **Changelog:** (Type what's new in this build)
6. Click **Run workflow** and the bot will instantly post it to the official channel!
