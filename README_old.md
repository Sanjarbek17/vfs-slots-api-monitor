# Browser Monitor with Selenium

This project contains Python scripts that use Selenium to create a Chrome browser instance and monitor user interactions in real-time.

## Files

1. **`browser_monitor.py`** - Advanced version with detailed logging and network monitoring
2. **`simple_browser_monitor.py`** - Basic version with simple activity tracking

## Features

### Advanced Monitor (`browser_monitor.py`)
- 🌐 Opens Chrome browser automatically
- 📝 Logs detailed activity including:
  - Page navigation
  - URL changes
  - Title changes
  - Browser console logs
  - Network activity
  - User interactions
- 💾 Saves logs to JSON file
- 🔍 Real-time monitoring
- 🎯 No terminal interaction needed - just browse!

### Simple Monitor (`simple_browser_monitor.py`)
- 🌐 Opens Chrome browser automatically
- 📝 Basic activity logging:
  - URL navigation
  - Page title changes
  - Timestamps
- 💾 Saves to text file
- 🎯 Easy to understand and modify
- 🚀 Zero setup - just run and browse!

## Installation

The required packages are already in `requirements.txt`. Make sure your virtual environment is activated:

```bash
# Activate virtual environment (if you have one)
source venv/bin/activate

# Install dependencies (if needed)
pip install -r requirements.txt
```

## Usage

### Running the Advanced Monitor

```bash
python browser_monitor.py
```

### Running the Simple Monitor

```bash
python simple_browser_monitor.py
```

## How it Works

1. **Browser Setup**: Automatically downloads and sets up ChromeDriver
2. **Auto-Open**: Opens Chrome browser with a new tab
3. **Real-time Monitoring**: Watches for:
   - Page changes
   - URL changes
   - User interactions
   - Network requests (advanced version)
4. **Browse Freely**: You can type URLs, click links, navigate normally
5. **Logging**: Records all activities with timestamps
6. **Saving**: Saves log files when you exit

## Example Output

```
🚀 Starting Browser Monitor
Setting up Chrome browser...
✅ Browser ready!
🌐 Opening Chrome browser...

🔍 Browser Monitor is now active!
📱 Use Chrome normally - all your activity is being logged
🌐 Navigate to any website, click links, type, etc.
⏹️  Press Ctrl+C in this terminal to stop monitoring

[14:30:15] 🚀 Browser opened - Ready for monitoring
[14:30:20] 📍 URL changed to: https://google.com
[14:30:21] 📄 Page title: Google
[14:30:25] 📍 URL changed to: https://google.com/search?q=python
```

## Log Files

- **Advanced version**: Creates JSON files with detailed activity data
- **Simple version**: Creates text files with basic activity logs
- Files are saved with timestamps: `activity_log_20250603_143022.json`

## Controls

- **Start monitoring**: Run the script and Chrome opens automatically
- **Browse normally**: Type URLs in address bar, click links, navigate freely  
- **Stop monitoring**: Press `Ctrl+C` in the terminal
- **Exit program**: Close the Chrome window or press `Ctrl+C`
- **View logs**: Check the generated log files for all activity

## Tips

1. The browser stays open for you to interact with
2. All your clicks, navigation, and page changes are logged
3. You can visit multiple URLs in one session
4. The program automatically handles ChromeDriver installation
5. Logs are saved automatically when you exit

## Troubleshooting

- Make sure Chrome browser is installed on your system
- If ChromeDriver issues occur, the script will auto-download the correct version
- Check the log files for detailed error information
