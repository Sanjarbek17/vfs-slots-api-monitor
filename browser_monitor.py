#!/usr/bin/env python3
"""
Browser Monitor with Selenium
This script creates a Chrome browser instance, allows URL input, and monitors user interactions.
"""

import time
import json
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
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("browser_activity.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class BrowserMonitor:
    def __init__(self):
        self.driver = None
        self.activity_log = []
        self.start_time = datetime.now()

    def setup_chrome(self):
        """Set up Chrome browser with monitoring capabilities"""
        try:
            chrome_options = Options()

            # Add options for better monitoring
            chrome_options.add_argument("--enable-logging")
            chrome_options.add_argument("--log-level=0")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option(
                "excludeSwitches", ["enable-automation"]
            )
            chrome_options.add_experimental_option("useAutomationExtension", False)

            # Try to enable performance logging with fallback
            try:
                # Enable performance logging to capture network activity
                chrome_options.add_experimental_option(
                    "perfLoggingPrefs",
                    {"enableNetwork": True, "enablePage": True},
                )
                chrome_options.set_capability(
                    "goog:loggingPrefs",
                    {"browser": "ALL", "driver": "ALL", "performance": "ALL"},
                )
                logger.info("Performance logging enabled")
            except Exception as perf_error:
                logger.warning(f"Performance logging not available: {perf_error}")
                # Fallback to basic logging only
                chrome_options.set_capability(
                    "goog:loggingPrefs",
                    {"browser": "ALL", "driver": "ALL"},
                )

            # Use WebDriver Manager to automatically handle ChromeDriver
            service = Service(ChromeDriverManager().install())

            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )

            logger.info("Chrome browser initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to setup Chrome: {str(e)}")
            # Try fallback setup with minimal options
            return self._setup_chrome_fallback()

    def _setup_chrome_fallback(self):
        """Fallback Chrome setup with minimal options"""
        try:
            logger.info("Attempting fallback Chrome setup...")
            chrome_options = Options()

            # Minimal options for basic functionality
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option(
                "excludeSwitches", ["enable-automation"]
            )

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            logger.info("Chrome browser initialized with fallback options")
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

    def monitor_page_changes(self):
        """Monitor for page changes and log them"""
        try:
            current_url = self.driver.current_url
            page_title = self.driver.title

            self.log_activity(
                "PAGE_INFO",
                {
                    "url": current_url,
                    "title": page_title,
                    "timestamp": datetime.now().isoformat(),
                },
            )

            # Get browser logs
            try:
                browser_logs = self.driver.get_log("browser")
                if browser_logs:
                    self.log_activity("BROWSER_LOGS", browser_logs[-5:])  # Last 5 logs
            except Exception as e:
                logger.debug(f"Browser logs not available: {e}")

            # Get performance logs (network activity)
            try:
                perf_logs = self.driver.get_log("performance")
                network_events = []
                for log in perf_logs:
                    try:
                        message = json.loads(log["message"])
                        if (
                            message.get("message", {})
                            .get("method", "")
                            .startswith("Network")
                        ):
                            network_events.append(message["message"])
                    except (json.JSONDecodeError, KeyError):
                        continue

                if network_events:
                    self.log_activity(
                        "NETWORK_ACTIVITY", network_events[-3:]
                    )  # Last 3 events
            except Exception as e:
                logger.debug(
                    f"Performance logs not available: {e}"
                )  # Changed to debug level

        except Exception as e:
            logger.warning(f"Error monitoring page: {str(e)}")

    def visit_url(self, url):
        """Visit the specified URL and log the action"""
        try:
            self.log_activity("NAVIGATION_START", f"Visiting: {url}")
            self.driver.get(url)

            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )

            self.log_activity("NAVIGATION_COMPLETE", f"Successfully loaded: {url}")
            self.monitor_page_changes()

        except TimeoutException:
            self.log_activity("NAVIGATION_TIMEOUT", f"Timeout loading: {url}")
        except Exception as e:
            self.log_activity("NAVIGATION_ERROR", f"Error loading {url}: {str(e)}")

    def monitor_user_activity(self):
        """Monitor user interactions in real-time"""
        print("\n" + "=" * 60)
        print("🔍 Browser Monitor is now active!")
        print("📱 Use Chrome normally - all your activity is being logged")
        print("🌐 Navigate to any website, click links, type, etc.")
        print("⏹️  Press Ctrl+C in this terminal to stop monitoring")
        print("🚪 Or simply close the Chrome window to end monitoring")
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

                # Monitor page periodically
                self.monitor_page_changes()

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
        filename = f"activity_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
        print("Starting Browser Monitor...")

        # Setup Chrome
        if not self.setup_chrome():
            print("Failed to start Chrome browser. Please check your setup.")
            return

        try:
            # Open Chromewe  with a completely blank page
            print("Opening Chrome browser...")
            self.driver.get("about:blank")
            self.log_activity("BROWSER_OPENED", "Chrome browser opened for monitoring")

            # Start monitoring user activity immediately
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

        print(f"\nTotal activities logged: {len(self.activity_log)}")
        print("Activity log saved. Session ended.")


if __name__ == "__main__":
    monitor = BrowserMonitor()
    monitor.run()
