# VFS Slots API Monitor

A collection of Python scripts for monitoring VFS Global visa application slots and news updates. This tool helps users track appointment slot availability and news updates from VFS Global.

## Features

- **Automated Authentication** (`AuthVFS.py`)
  - Handles login to VFS Global website
  - Extracts and manages JWT tokens
  - Uses Selenium for browser automation
  - Supports CAPTCHA solving

- **Appointment Slot Monitoring** (`PingVFS.py`)
  - Continuously monitors for available appointment slots
  - Sends desktop notifications when slots are found
  - Plays sound alerts for immediate attention
  - Logs all responses for tracking

- **News Updates** (`NewsVFS.py`)
  - Monitors VFS Global news feed
  - Notifies about new articles and announcements
  - Displays news content in terminal
  - Sound notifications for updates

## Requirements

- Python 3.x
- Chrome/Chromium browser
- Required Python packages:
  - selenium
  - requests
  - pygame
  - playsound (for Windows)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/vfs-slots-api-monitor.git
cd vfs-slots-api-monitor
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install selenium requests pygame playsound
```


![Screenshot](screenshot.png)

## Installation
This project is developed following the quote _"Code is the best documentation"_, therefore it's better you work it out yourself by analyzing the codebase.

Hints-
- These scripts are crafted for _Linux_ machines.
- You need `python3` installed and configured in you machine.
- Selenium and ChromeWebdriver needed to be installed in the machine.
- For using the `monitor` UX `tmux` also needed to be installed in the machine.
- Understand the `monitor`, `.gitignore` file and the `main()` function of the `*.py` files.
- Rename the `example.*.json` files to `*.json` and set necessary credentials in there.
- Place a `*.mp3` music file as `alert.mp3` in the project root directory.

## Configuration

1. Copy the example configuration files:
```bash
cp example.auth_creds.json auth_creds.json
cp example.ping_creds.json ping_creds.json
cp example.news_creds.json news_creds.json
```

2. Edit the configuration files with your details:
- `auth_creds.json`: VFS login credentials
- `ping_creds.json`: Appointment monitoring settings
- `news_creds.json`: News monitoring settings

## Usage

Run the monitor script with or without news monitoring:

```bash
# Without news monitoring
./monitor

# With news monitoring
./monitor --with-news
```

The script will:
1. Start authentication process
2. Monitor for appointment slots
3. Monitor news updates (if enabled)
4. Send notifications for any changes

## Understanding the Output

- `.` (dots): Indicates active monitoring
- Notifications: Desktop notifications for updates
- Sound alerts: Plays when slots are found
- Terminal output: Detailed information and status

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## Troubleshooting

- **Authentication Issues**: Check your credentials in `auth_creds.json`
- **CAPTCHA**: The script will pause for manual CAPTCHA solving
- **Sound not working**: Ensure system volume is on and audio device is working

## Disclaimer

This tool is for personal use only. Please respect VFS Global's terms of service and rate limiting policies.
