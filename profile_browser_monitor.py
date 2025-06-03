#!/usr/bin/env python3
"""
Browser Monitor with Default Profile
This version opens Chrome with your default profile and monitors activity.
"""

import time
import json
import os
import psutil
import platform
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Set up logging
os.makedirs("activity_log", exist_ok=True)  # Ensure activity_log folder exists
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("activity_log/profile_browser_activity.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class ProfileBrowserMonitor:
    def __init__(self):
        self.driver = None
        self.activity_log = []
        self.start_time = datetime.now()
        self.last_url = ""
        self.last_title = ""

    def get_chrome_profile_path(self):
        """Get the default Chrome profile path based on the operating system"""
        system = platform.system()

        if system == "Darwin":  # macOS
            return "/Users/{}/Library/Application Support/Google/Chrome".format(
                os.getenv("USER")
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

    def setup_chrome_with_profile(self):
        """Set up Chrome browser with default profile"""
        try:
            chrome_options = Options()

            # Get the Chrome profile path
            profile_path = self.get_chrome_profile_path()

            # First try to connect to existing Chrome with remote debugging
            if self.is_chrome_running():
                logger.info(
                    "Chrome is already running. Attempting to connect via remote debugging..."
                )
                try:
                    chrome_options.add_experimental_option(
                        "debuggerAddress", "127.0.0.1:9222"
                    )
                    service = Service(ChromeDriverManager().install())
                    self.driver = webdriver.Chrome(
                        service=service, options=chrome_options
                    )
                    logger.info("✓ Successfully connected to existing Chrome instance")
                    return True
                except Exception as debug_error:
                    logger.warning(
                        f"Could not connect to existing Chrome via debugging: {debug_error}"
                    )
                    logger.info(
                        "Will close existing Chrome and start new instance with profile..."
                    )
                    # Kill existing Chrome processes to access profile
                    os.system("pkill -f 'Google Chrome'")
                    time.sleep(3)  # Wait for processes to close

            # Start new Chrome instance with profile
            if profile_path and os.path.exists(profile_path):
                logger.info(f"Starting Chrome with profile: {profile_path}")

                # Use the default profile
                chrome_options.add_argument(f"--user-data-dir={profile_path}")
                chrome_options.add_argument("--profile-directory=Default")
            else:
                logger.warning(
                    "Could not find Chrome profile path. Using temporary profile."
                )

            # Add options for better monitoring and stability
            chrome_options.add_argument("--enable-logging")
            chrome_options.add_argument("--log-level=0")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--remote-debugging-port=9222")
            chrome_options.add_argument("--remote-allow-origins=*")

            # Performance logging for network monitoring (newer format)
            chrome_options.set_capability(
                "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
            )

            # Create WebDriver service
            service = Service(ChromeDriverManager().install())

            # Initialize the driver
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            # Execute script to remove webdriver property
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )

            logger.info("✓ Chrome browser with profile setup completed successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to setup Chrome with profile: {e}")
            return self.setup_fallback_chrome()

    def setup_fallback_chrome(self):
        """Fallback Chrome setup without profile"""
        try:
            logger.info("Setting up fallback Chrome without profile...")
            chrome_options = Options()

            # Basic options (using compatible format)
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            # Performance logging (compatible format)
            chrome_options.set_capability(
                "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
            )

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            # Execute script to remove webdriver property
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )

            logger.info("Fallback Chrome setup completed")
            return True

        except Exception as e:
            logger.error(f"Fallback Chrome setup failed: {e}")
            return False

    def log_activity(self, activity_type, details):
        """Log browsing activity"""
        timestamp = datetime.now()
        activity = {
            "timestamp": timestamp.isoformat(),
            "type": activity_type,
            "details": details,
            "url": self.driver.current_url if self.driver else "N/A",
            "title": self.driver.title if self.driver else "N/A",
        }

        self.activity_log.append(activity)
        logger.info(f"[{activity_type}] {details}")

        # Save to file
        self.save_activity_log()

    def save_activity_log(self):
        """Save activity log to JSON file"""
        try:
            os.makedirs(
                "activity_log", exist_ok=True
            )  # Ensure activity_log folder exists
            with open("activity_log/profile_browser_activity.json", "w") as f:
                json.dump(self.activity_log, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save activity log: {e}")

    def monitor_browsing(self):
        """Monitor browsing activity in real-time"""
        logger.info("Starting browsing activity monitoring...")

        try:
            while True:
                if not self.driver:
                    break

                try:
                    current_url = self.driver.current_url
                    current_title = self.driver.title

                    # Check for URL changes
                    if current_url != self.last_url:
                        self.log_activity("URL_CHANGE", f"Navigated to: {current_url}")
                        self.last_url = current_url

                    # Check for title changes
                    if current_title != self.last_title:
                        self.log_activity(
                            "TITLE_CHANGE", f"Page title: {current_title}"
                        )
                        self.last_title = current_title

                    # Get performance logs
                    try:
                        logs = self.driver.get_log("performance")
                        for log in logs:
                            message = json.loads(log["message"])
                            if (
                                message["message"]["method"]
                                == "Network.responseReceived"
                            ):
                                response = message["message"]["params"]["response"]
                                if response["status"] >= 400:
                                    self.log_activity(
                                        "HTTP_ERROR",
                                        f"HTTP {response['status']}: {response['url']}",
                                    )
                    except Exception:
                        pass  # Ignore performance log errors

                    time.sleep(1)  # Check every second

                except WebDriverException as e:
                    logger.error(f"WebDriver error during monitoring: {e}")
                    break
                except Exception as e:
                    logger.error(f"Unexpected error during monitoring: {e}")
                    time.sleep(1)

        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")

    def start_monitoring(self):
        """Start the browser monitoring process"""
        try:
            logger.info("=== Profile Browser Monitor Starting ===")

            # Setup Chrome with profile
            if not self.setup_chrome_with_profile():
                logger.error("Failed to setup Chrome browser")
                return

            # Open with blank page
            self.driver.get("about:blank")
            self.log_activity("BROWSER_START", "Chrome browser opened with profile")

            # Start monitoring
            self.monitor_browsing()

        except KeyboardInterrupt:
            logger.info("Monitoring interrupted by user")
        except Exception as e:
            logger.error(f"Error during monitoring: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            try:
                self.log_activity("BROWSER_CLOSE", "Browser session ended")
                self.driver.quit()
                logger.info("Browser closed successfully")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")

        # Final save of activity log
        self.save_activity_log()
        logger.info(
            f"Monitoring session completed. Total activities logged: {len(self.activity_log)}"
        )


def main():
    """Main function to run the profile browser monitor"""
    monitor = ProfileBrowserMonitor()

    try:
        monitor.start_monitoring()
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"Program error: {e}")
    finally:
        monitor.cleanup()


if __name__ == "__main__":
    main()
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("browser_activity.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class ProfileBrowserMonitor:
    def __init__(self):
        self.driver = None
        self.activity_log = []
        self.start_time = datetime.now()
        self.chrome_profile_path = os.path.expanduser(
            "~/Library/Application Support/Google/Chrome"
        )

    def is_chrome_running(self):
        """Check if Chrome is already running"""
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if "chrome" in proc.info["name"].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False

    def setup_chrome(self):
        """Set up Chrome browser with default profile"""
        try:
            chrome_options = Options()

            # Check if Chrome is running and warn user
            if self.is_chrome_running():
                print(
                    "⚠️  Chrome is already running. This might interfere with profile access."
                )
                print(
                    "💡 For best results, close all Chrome windows before running this script."
                )
                response = input("Continue anyway? (y/n): ").strip().lower()
                if response != "y":
                    return False

            # Use default Chrome profile
            if os.path.exists(self.chrome_profile_path):
                chrome_options.add_argument(
                    f"--user-data-dir={self.chrome_profile_path}"
                )
                chrome_options.add_argument("--profile-directory=Default")
                logger.info(
                    "Using default Chrome profile with your bookmarks and extensions"
                )
            else:
                logger.warning(
                    "Default Chrome profile not found, using temporary profile"
                )

            # Add monitoring options
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option(
                "excludeSwitches", ["enable-automation"]
            )
            chrome_options.add_experimental_option("useAutomationExtension", False)

            # Enable basic logging
            chrome_options.add_experimental_option(
                "perfLoggingPrefs", {"enableNetwork": True}
            )
            chrome_options.set_capability(
                "goog:loggingPrefs", {"browser": "ALL", "performance": "ALL"}
            )

            # Use WebDriver Manager
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            # Hide automation indicators
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )

            logger.info("Chrome browser with default profile initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to setup Chrome with profile: {str(e)}")
            return self._setup_chrome_fallback()

    def _setup_chrome_fallback(self):
        """Fallback Chrome setup without profile"""
        try:
            logger.info("Attempting fallback Chrome setup without profile...")
            chrome_options = Options()

            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option(
                "excludeSwitches", ["enable-automation"]
            )

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            logger.info("Chrome browser initialized with temporary profile")
            return True

        except Exception as e:
            logger.error(f"Fallback setup also failed: {str(e)}")
            return False

    def log_activity(self, activity_type, details):
        """Log user activity with timestamp"""
        timestamp = datetime.now()
        activity = {
            "timestamp": timestamp.isoformat(),
            "type": activity_type,
            "details": details,
            "url": self.driver.current_url if self.driver else "N/A",
        }

        self.activity_log.append(activity)
        logger.info(f"Activity: {activity_type} - {details}")

    def monitor_user_activity(self):
        """Monitor user interactions in real-time"""
        print("\n" + "=" * 60)
        print("🔍 Browser Monitor with Default Profile Active!")
        print("👤 Using your Chrome profile (bookmarks, extensions, etc.)")
        print("🌐 Browse normally - all activity is being logged")
        print("⏹️  Press Ctrl+C to stop monitoring")
        print("🚪 Or close the Chrome window to end")
        print("=" * 60)

        last_url = ""
        last_title = ""

        try:
            while True:
                current_url = self.driver.current_url
                current_title = self.driver.title

                # Check for URL changes
                if current_url != last_url:
                    self.log_activity(
                        "URL_CHANGE", {"from": last_url, "to": current_url}
                    )
                    last_url = current_url

                # Check for title changes
                if current_title != last_title:
                    self.log_activity(
                        "TITLE_CHANGE", {"from": last_title, "to": current_title}
                    )
                    last_title = current_title

                # Check if browser is still open
                try:
                    self.driver.current_window_handle
                except:
                    logger.info("Browser window closed by user")
                    break

                time.sleep(2)  # Check every 2 seconds

        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Error during monitoring: {str(e)}")

    def save_activity_log(self):
        """Save activity log to file"""
        filename = f"profile_activity_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, "w") as f:
                json.dump(
                    {
                        "session_start": self.start_time.isoformat(),
                        "session_end": datetime.now().isoformat(),
                        "total_activities": len(self.activity_log),
                        "activities": self.activity_log,
                    },
                    f,
                    indent=2,
                )
            logger.info(f"Activity log saved to: {filename}")
        except Exception as e:
            logger.error(f"Failed to save activity log: {str(e)}")

    def run(self):
        """Main execution method"""
        print("🚀 Starting Browser Monitor with Default Profile...")

        # Setup Chrome
        if not self.setup_chrome():
            print("❌ Failed to start Chrome browser. Please check your setup.")
            return

        try:
            # Open with blank page
            print("🌐 Opening Chrome with your default profile...")
            self.driver.get("about:blank")
            self.log_activity("BROWSER_OPENED", "Chrome opened with default profile")

            # Start monitoring
            self.monitor_user_activity()

        except KeyboardInterrupt:
            logger.info("Program interrupted by user")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Browser closed")
            except:
                pass

        # Save activity log
        self.save_activity_log()
        print(f"\n✅ Total activities logged: {len(self.activity_log)}")
        print("📁 Activity log saved. Session ended.")


if __name__ == "__main__":
    monitor = ProfileBrowserMonitor()
    monitor.run()
