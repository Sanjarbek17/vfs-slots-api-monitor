# Authentication Setup Guide

## 1. Initial Requirements
- Chrome browser installed
- Python virtual environment activated
- Required packages installed

## 2. Configuration Steps

### 2.1 Install Required Packages
```bash
# Activate virtual environment if not already activated
source venv/bin/activate

# Install required packages
pip install selenium requests undetected-chromedriver
```

### 2.2 Set Up Authentication Credentials

1. Copy the example configuration:
```bash
cp example.auth_creds.json auth_creds.json
```

2. Edit `auth_creds.json` with your credentials:
```json
{
    "url": "https://visa.vfsglobal.com/bgd/en/dnk/login",
    "email_id": "//*[@id=\"mat-input-0\"]",
    "password_id": "//*[@id=\"mat-input-1\"]",
    "ensure_login": "//*[contains(text(), 'Start New Booking')]",
    "submit": "//*[contains(text(), 'Sign In')]",
    "user": "YOUR_EMAIL",
    "pass": "YOUR_PASSWORD",
    "auth_path": "./auth.txt",
    "refr_delay": 600,
    "avrg_delay": 10
}
```

Replace:
- `YOUR_EMAIL`: Your VFS Global account email
- `YOUR_PASSWORD`: Your VFS Global account password

The other fields are:
- `refr_delay`: Time between token refresh attempts (in seconds)
- `avrg_delay`: Average delay between actions (in seconds)

### 2.3 Verify Setup

1. Test authentication separately:
```bash
python3 AuthVFS.py
```

This will:
- Open Chrome browser
- Attempt to log in to VFS Global
- Generate JWT token in `auth.txt`

### 2.4 Handle CAPTCHA

When you run the script for the first time:
1. Chrome will open automatically
2. Enter your credentials
3. If CAPTCHA appears:
   - Solve it manually
   - The script will wait for you
   - After solving, login will continue automatically

### 2.5 Common XPath Issues

If login fails, you might need to update XPath selectors. To find correct XPath:
1. Open VFS website in Chrome
2. Right-click on the email field
3. Inspect element
4. Right-click on the highlighted HTML
5. Copy -> Copy XPath
6. Update `email_id` and `password_id` in `auth_creds.json`

Current working XPaths for most regions:
```json
{
    "email_id": "//*[@id=\"mat-input-0\"]",
    "password_id": "//*[@id=\"mat-input-1\"]",
    "ensure_login": "//*[contains(text(), 'Start New Booking')]",
    "submit": "//*[contains(text(), 'Sign In')]"
}
```

### 2.6 Configuration Parameters Explained

- `url`: VFS login URL for your country/region
- `email_id`: XPath to email input field
- `password_id`: XPath to password input field
- `ensure_login`: XPath to verify successful login
- `submit`: XPath to submit button
- `auth_path`: Where to store JWT token
- `refr_delay`: Refresh delay (600 = 10 minutes)
- `avrg_delay`: Action delay (10 seconds recommended)

### 2.7 Troubleshooting

1. **Login Fails Immediately:**
   - Check credentials
   - Verify XPath selectors
   - Increase `avrg_delay`

2. **CAPTCHA Issues:**
   - Don't rush CAPTCHA solving
   - Wait for page to load fully
   - Check Chrome window is visible

3. **JWT Not Generated:**
   - Check `auth.txt` exists
   - Verify file permissions
   - Check console for errors

4. **Browser Crashes:**
   - Update Chrome
   - Clear browser cache
   - Check `undetected-chromedriver` version
