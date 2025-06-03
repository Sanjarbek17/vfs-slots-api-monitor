# Browser Monitor with Selenium

A comprehensive Python-based browser monitoring solution that opens Chrome with your default profile and tracks user browsing activity in real-time using Selenium WebDriver.

## Features

- ✅ **Profile-Based Monitoring**: Uses your default Chrome profile with all bookmarks, extensions, and settings
- ✅ **Real-Time Activity Logging**: Monitors URL changes, page titles, and network activity
- ✅ **Multiple Monitor Types**: Simple, advanced, and profile-aware monitoring scripts
- ✅ **Chrome Profile Launcher**: Helper utility to launch Chrome with proper debugging support
- ✅ **Automatic ChromeDriver Management**: Uses WebDriverManager for seamless driver updates
- ✅ **Robust Error Handling**: Fallback mechanisms for various Chrome setup scenarios
- ✅ **Cross-Platform Support**: Works on macOS, Windows, and Linux

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Dependencies include:
   - `selenium` - Browser automation
   - `webdriver-manager` - Automatic ChromeDriver management
   - `psutil` - Process monitoring

## Usage

### Option 1: Profile Browser Monitor (Recommended)

This is the most comprehensive solution that uses your default Chrome profile:

```bash
python profile_browser_monitor.py
```

**Features:**
- Uses your default Chrome profile (bookmarks, extensions, etc.)
- Attempts to connect to existing Chrome instances via remote debugging
- Falls back to creating new Chrome instance if needed
- Logs all activity to `profile_browser_activity.log` and `profile_browser_activity.json`

### Option 2: Chrome Profile Launcher + Monitor

For better control over Chrome startup:

1. **First, launch Chrome with your profile:**
```bash
python chrome_profile_launcher.py
```
Choose option 1 to launch Chrome with profile + remote debugging enabled.

2. **Then run the profile monitor:**
```bash
python profile_browser_monitor.py
```

### Option 3: Simple Browser Monitor

For basic monitoring without profile complications:

```bash
python simple_browser_monitor.py
```

### Option 4: Advanced Browser Monitor

For advanced monitoring with extensive logging:

```bash
python browser_monitor.py
```

## Scripts Overview

### `profile_browser_monitor.py`
- **Best for**: Full-featured monitoring with your Chrome profile
- **Features**: Profile detection, remote debugging connection, comprehensive logging
- **Output**: `activity_log/profile_browser_activity.log`, `activity_log/profile_browser_activity.json`

### `chrome_profile_launcher.py`
- **Best for**: Launching Chrome with proper debugging setup
- **Features**: Interactive launcher, profile path detection, debugging port setup
- **Use case**: Preparation for profile-based monitoring

### `simple_browser_monitor.py`
- **Best for**: Quick testing and basic monitoring
- **Features**: Minimal setup, basic activity logging
- **Output**: `activity_log/simple_activity_*.txt`

### `browser_monitor.py`
- **Best for**: Advanced users who need detailed network monitoring
- **Features**: Performance logging, network activity tracking, advanced Chrome options
- **Output**: `activity_log/browser_activity.log`, `activity_log/activity_log_*.json`

## How It Works

### Profile Detection
The system automatically detects your Chrome profile location:
- **macOS**: `~/Library/Application Support/Google/Chrome`
- **Windows**: `%LOCALAPPDATA%\Google\Chrome\User Data`
- **Linux**: `~/.config/google-chrome`

### Chrome Integration
1. **Profile Access**: Launches Chrome with `--user-data-dir` pointing to your profile
2. **Remote Debugging**: Uses `--remote-debugging-port=9222` for connection
3. **WebDriver Control**: Selenium controls the browser while preserving your profile

### Activity Monitoring
- **URL Changes**: Tracks navigation between pages
- **Title Changes**: Monitors page title updates
- **Network Activity**: Logs HTTP requests and responses
- **Error Detection**: Captures HTTP errors and failed requests

## Output Files

All activity logs are now organized in the `activity_log/` folder for better organization.

### JSON Logs
```json
{
  "timestamp": "2025-06-03T10:57:55.956789",
  "type": "URL_CHANGE",
  "details": "Navigated to: https://example.com",
  "url": "https://example.com",
  "title": "Example Page"
}
```

### Text Logs
```
2025-06-03 10:57:55,957 - INFO - [BROWSER_START] Chrome browser opened with profile
2025-06-03 10:57:55,966 - INFO - [URL_CHANGE] Navigated to: about:blank
```

### Log File Organization
- `activity_log/browser_activity.log` - Main browser monitor log file
- `activity_log/activity_log_YYYYMMDD_HHMMSS.json` - Detailed JSON activity logs
- `activity_log/profile_browser_activity.log` - Profile monitor log file  
- `activity_log/profile_browser_activity.json` - Profile monitor JSON data
- `activity_log/simple_activity_YYYYMMDD_HHMMSS.txt` - Simple monitor text logs

## Troubleshooting

### Chrome Profile Issues
- **Error**: "Chrome profile locked"
- **Solution**: Close all Chrome instances before running the monitor, or use the Chrome Profile Launcher

### Remote Debugging Connection
- **Error**: "Cannot connect to existing Chrome"
- **Solution**: Launch Chrome with debugging enabled using `chrome_profile_launcher.py`

### ChromeDriver Issues
- **Error**: "ChromeDriver version mismatch"
- **Solution**: WebDriverManager handles this automatically, but you can clear cache in `~/.wdm/`

### Permission Issues
- **Error**: "Access denied to Chrome profile"
- **Solution**: Ensure Chrome is completely closed and you have read/write access to the profile directory

## Advanced Configuration

### Custom Profile Path
Edit the `get_chrome_profile_path()` method in any script to use a custom profile location.

### Custom Logging
Modify the logging configuration to change output format, level, or destination.

### Chrome Options
Add custom Chrome arguments in the `setup_chrome*()` methods for specific needs.

## Security Notes

- The monitoring scripts have access to your browsing data through the Chrome profile
- Network logs may contain sensitive information
- Use responsibly and in compliance with privacy policies
- Consider using temporary profiles for sensitive testing

## Platform-Specific Notes

### macOS
- May require granting Terminal access to control Chrome
- Chrome path: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`

### Windows
- May require running as Administrator for full Chrome control
- Chrome path: `C:\Program Files\Google\Chrome\Application\chrome.exe`

### Linux
- Chrome executable path may vary by distribution
- Common path: `/usr/bin/google-chrome`

## Example Usage

1. **Quick Start with Profile**:
   ```bash
   python profile_browser_monitor.py
   ```

2. **Manual Chrome Setup**:
   ```bash
   python chrome_profile_launcher.py
   # Choose option 1, then in another terminal:
   python profile_browser_monitor.py
   ```

3. **Simple Monitoring**:
   ```bash
   python simple_browser_monitor.py
   ```

## License

This project is for educational and monitoring purposes. Use responsibly and in accordance with applicable laws and Chrome's terms of service.
