#!/usr/bin/env python3
"""
Chrome Profile Launcher
This script helps launch Chrome with the default profile and remote debugging enabled,
allowing the browser monitor to connect to it.
"""

import os
import platform
import subprocess
import time
import psutil
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class ChromeProfileLauncher:
    def __init__(self):
        self.chrome_path = self.get_chrome_path()
        self.profile_path = self.get_chrome_profile_path()

    def get_chrome_path(self):
        """Get Chrome executable path based on OS"""
        system = platform.system()

        if system == "Darwin":  # macOS
            return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        elif system == "Windows":
            return "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        elif system == "Linux":
            return "/usr/bin/google-chrome"
        else:
            return None

    def get_chrome_profile_path(self):
        """Get the default Chrome profile path based on the operating system"""
        system = platform.system()

        if system == "Darwin":  # macOS
            return (
                f"/Users/{os.getenv('USER')}/Library/Application Support/Google/Chrome"
            )
        elif system == "Windows":
            return os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
        elif system == "Linux":
            return os.path.expanduser("~/.config/google-chrome")
        else:
            return None

    def is_chrome_running(self):
        """Check if Chrome is already running"""
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if "chrome" in proc.info["name"].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False

    def close_chrome(self):
        """Close all Chrome processes"""
        logger.info("Closing existing Chrome processes...")

        if platform.system() == "Darwin":
            os.system("pkill -f 'Google Chrome'")
        elif platform.system() == "Windows":
            os.system("taskkill /f /im chrome.exe")
        else:
            os.system("pkill -f chrome")

        time.sleep(3)  # Wait for processes to close

    def launch_chrome_with_debugging(self):
        """Launch Chrome with default profile and remote debugging enabled"""
        try:
            if not self.chrome_path or not os.path.exists(self.chrome_path):
                logger.error(f"Chrome not found at: {self.chrome_path}")
                return False

            if not self.profile_path or not os.path.exists(self.profile_path):
                logger.error(f"Chrome profile not found at: {self.profile_path}")
                return False

            # Close existing Chrome instances
            if self.is_chrome_running():
                self.close_chrome()

            # Chrome launch arguments
            chrome_args = [
                self.chrome_path,
                f"--user-data-dir={self.profile_path}",
                "--profile-directory=Default",
                "--remote-debugging-port=9222",
                "--remote-allow-origins=*",
                "--disable-web-security",
                "--allow-running-insecure-content",
                "about:blank",
            ]

            logger.info("Launching Chrome with profile and remote debugging...")
            logger.info(f"Profile path: {self.profile_path}")
            logger.info("Remote debugging port: 9222")

            # Launch Chrome
            subprocess.Popen(chrome_args)

            # Wait a moment for Chrome to start
            time.sleep(3)

            if self.is_chrome_running():
                logger.info(
                    "✓ Chrome launched successfully with profile and debugging enabled"
                )
                logger.info(
                    "You can now run the profile browser monitor to connect to this Chrome instance"
                )
                return True
            else:
                logger.error("Failed to launch Chrome")
                return False

        except Exception as e:
            logger.error(f"Error launching Chrome: {e}")
            return False

    def launch_chrome_normal(self):
        """Launch Chrome normally with default profile (no debugging)"""
        try:
            if not self.chrome_path or not os.path.exists(self.chrome_path):
                logger.error(f"Chrome not found at: {self.chrome_path}")
                return False

            if not self.profile_path or not os.path.exists(self.profile_path):
                logger.error(f"Chrome profile not found at: {self.profile_path}")
                return False

            # Chrome launch arguments
            chrome_args = [
                self.chrome_path,
                f"--user-data-dir={self.profile_path}",
                "--profile-directory=Default",
                "about:blank",
            ]

            logger.info("Launching Chrome with default profile...")
            logger.info(f"Profile path: {self.profile_path}")

            # Launch Chrome
            subprocess.Popen(chrome_args)

            # Wait a moment for Chrome to start
            time.sleep(2)

            if self.is_chrome_running():
                logger.info("✓ Chrome launched successfully with default profile")
                return True
            else:
                logger.error("Failed to launch Chrome")
                return False

        except Exception as e:
            logger.error(f"Error launching Chrome: {e}")
            return False


def main():
    """Main function"""
    launcher = ChromeProfileLauncher()

    print("Chrome Profile Launcher")
    print("=======================")
    print("1. Launch Chrome with profile + remote debugging (for monitoring)")
    print("2. Launch Chrome with profile only (normal browsing)")
    print("3. Close all Chrome instances")
    print("4. Exit")

    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()

            if choice == "1":
                launcher.launch_chrome_with_debugging()
            elif choice == "2":
                launcher.launch_chrome_normal()
            elif choice == "3":
                launcher.close_chrome()
                logger.info("Chrome instances closed")
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1-4.")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")


if __name__ == "__main__":
    main()
