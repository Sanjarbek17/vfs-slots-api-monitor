# VFS Slots API Monitor - User Guide

This guide will help you set up and use the VFS Slots API Monitor effectively.

## Initial Setup

1. **System Requirements**
   - macOS or Linux operating system
   - Python 3.x installed
   - Chrome/Chromium browser
   - `tmux` installed (for the monitor interface)

2. **Install Dependencies**
   ```bash
   # Create and activate virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install required packages
   pip install selenium requests pygame undetected-chromedriver
   ```

3. **Configure Sound Alert**
   - Place any MP3 file as `alert.mp3` in the project root directory
   - This will be played when slots are found or news updates appear

## Configuration

1. **Set up Authentication (`auth_creds.json`)**
   ```json
   {
     "url": "https://visa.vfsglobal.com/your-country/login",
     "email_id": "//input[@name='email']",
     "password_id": "//input[@name='password']",
     "ensure_login": "//div[contains(@class, 'logged-in')]",
     "submit": "//button[@type='submit']",
     "user": "YOUR_EMAIL",
     "pass": "YOUR_PASSWORD",
     "auth_path": "./auth.txt",
     "refr_delay": 600,
     "avrg_delay": 10
   }
   ```

2. **Configure Slot Monitoring (`ping_creds.json`)**
   ```json
   {
     "url": "https://lift-api.vfsglobal.com/appointment/slots",
     "urlparams": {
       "countryCode": "YOUR_COUNTRY",
       "missionCode": "YOUR_MISSION",
       "centerCode": "YOUR_CENTER",
       "loginUser": "YOUR_EMAIL",
       "visaCategoryCode": "YOUR_CATEGORY",
       "languageCode": "en-US",
       "applicantsCount": "1",
       "days": "90",
       "slotType": "2"
     },
     "paths": {
       "auth": "./auth.txt",
       "output": "./output.txt"
     },
     "sound": "./alert.mp3"
   }
   ```

3. **Set up News Monitoring (`news_creds.json`)**
   ```json
   {
     "url": "https://visa.vfsglobal.com/api/news",
     "urlparams": {
       "content_type": "countryNews",
       "fields.locale": "your-country-code",
       "fields.permanent": true
     },
     "headers": {
       "Authorization": "Bearer YOUR_TOKEN",
       "Content-Type": "application/json"
     },
     "max_num": 10,
     "delay": 60,
     "sound": "./alert.mp3"
   }
   ```

## Running the Monitor

1. **Basic Monitoring (Slots Only)**
   ```bash
   ./monitor
   ```
   This will:
   - Start the authentication process
   - Monitor for available slots
   - Display progress with dots (.)
   - Play sound and show notification when slots are found

2. **Full Monitoring (Slots + News)**
   ```bash
   ./monitor --with-news
   ```
   Additional features:
   - Monitors VFS news updates
   - Notifies about new articles
   - Shows news content in terminal

## Understanding the Interface

The monitor uses `tmux` to create a split-screen view:

```
┌─────────────┬─────────────┐
│ Auth Status │ Slot Monitor│
├─────────────┤             │
│ News Feed   │             │
└─────────────┴─────────────┘
```

- **Top Left**: Authentication status and JWT generation
- **Bottom Left**: News updates (if enabled)
- **Right**: Slot monitoring progress

## Monitoring Progress

1. **Authentication Window**
   - A Chrome window will open for login
   - You may need to solve CAPTCHA manually
   - The window remains open to maintain session

2. **Progress Indicators**
   - Dots (.) show active monitoring
   - Each dot represents one check
   - Notifications appear on your desktop
   - Sound plays for important events

3. **Output File**
   - All responses are logged to `output.txt`
   - Use this for debugging or tracking history

## Troubleshooting

1. **Authentication Issues**
   - Check your credentials in `auth_creds.json`
   - Ensure the XPath selectors match VFS website
   - Try increasing `avrg_delay` if login fails

2. **No Slots Found**
   - Verify your `ping_creds.json` parameters
   - Check `output.txt` for API responses
   - Ensure JWT token is being generated

3. **Sound Not Working**
   - Check if `alert.mp3` exists
   - Test system sound
   - Verify pygame installation

4. **CAPTCHA Handling**
   - When CAPTCHA appears, solve it manually
   - The script will wait for completion
   - Session continues after CAPTCHA

## Best Practices

1. **Rate Limiting**
   - Use reasonable delays (minimum 5-10 seconds)
   - Don't run multiple instances
   - Respect VFS terms of service

2. **Session Management**
   - Keep the Chrome window open
   - Don't interfere with the automated process
   - Let CAPTCHA solving complete fully

3. **Monitoring**
   - Check `output.txt` periodically
   - Keep system volume on for alerts
   - Ensure stable internet connection

## Common Configurations

1. **High-Frequency Monitoring**
   ```json
   {
     "refr_delay": 300,
     "avrg_delay": 5
   }
   ```

2. **Conservative Monitoring**
   ```json
   {
     "refr_delay": 900,
     "avrg_delay": 15
   }
   ```

Remember: Be responsible with your monitoring frequency to avoid overwhelming the VFS servers or getting your IP blocked.
