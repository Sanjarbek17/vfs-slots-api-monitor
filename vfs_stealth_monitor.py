#!/usr/bin/env python3
"""
VFS Global Stealth Browser Monitor
Enhanced browser monitor specifically designed to bypass VFS Global's bot detection
"""

import time
import json
import random
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
import psutil
import os

# Set up logging
os.makedirs("activity_log", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("activity_log/vfs_stealth_activity.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class VFSStealthMonitor:
    def __init__(self):
        self.driver = None
        self.activity_log = []
        self.start_time = datetime.now()

    def is_chrome_running(self):
        """Check if Chrome is already running"""
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                if "chrome" in proc.info["name"].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False

    def setup_ultra_stealth_chrome(self):
        """Setup Chrome with maximum stealth for VFS Global"""
        try:
            # Ensure Chrome is closed first
            if self.is_chrome_running():
                print("🛑 Chrome is running. Please close ALL Chrome windows first!")
                print("This is critical for VFS Global to work properly.")
                response = input("Continue anyway? (y/n): ").strip().lower()
                if response != "y":
                    return False

            chrome_options = Options()

            # Use a completely clean profile
            import tempfile

            temp_profile = tempfile.mkdtemp(prefix="vfs_chrome_")
            chrome_options.add_argument(f"--user-data-dir={temp_profile}")

            print(f"🔒 Using temporary clean profile: {temp_profile}")

            # Maximum stealth options
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option(
                "excludeSwitches", ["enable-automation"]
            )
            chrome_options.add_experimental_option("useAutomationExtension", False)

            # Remove automation indicators
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--no-first-run")
            chrome_options.add_argument("--no-default-browser-check")
            chrome_options.add_argument("--disable-default-apps")

            # Disable automation detection features
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--disable-ipc-flooding-protection")

            # Make it look like a real user
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-renderer-backgrounding")

            # Real user agent (latest Chrome on macOS)
            real_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            chrome_options.add_argument(f"--user-agent={real_user_agent}")

            # Set window size to common resolution
            chrome_options.add_argument("--window-size=1920,1080")

            # Disable logging that might be detected
            chrome_options.add_argument("--disable-logging")
            chrome_options.add_argument("--log-level=3")
            chrome_options.add_argument("--silent")

            # Additional stealth
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-features=TranslateUI")
            chrome_options.add_argument("--disable-features=BlinkGenPropertyTrees")

            # Create service
            service = Service(ChromeDriverManager().install())

            # Initialize driver
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            # Execute maximum stealth scripts
            self.apply_stealth_scripts()

            logger.info("Ultra stealth Chrome initialized for VFS Global")
            print("✅ VFS Global stealth mode activated!")
            return True

        except Exception as e:
            logger.error(f"Failed to setup stealth Chrome: {str(e)}")
            return False

    def apply_stealth_scripts(self):
        """Apply JavaScript to hide all automation traces"""
        try:
            # Hide webdriver property
            self.driver.execute_script(
                """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
            """
            )

            # Override Chrome automation properties
            self.driver.execute_script(
                """
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en'],
                });
                Object.defineProperty(navigator, 'platform', {
                    get: () => 'MacIntel',
                });
                Object.defineProperty(navigator, 'hardwareConcurrency', {
                    get: () => 8,
                });
            """
            )

            # Override automation detection functions
            self.driver.execute_script(
                """
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
            """
            )

            # Override CDP runtime
            self.driver.execute_script(
                """
                delete window.chrome.runtime.onConnect;
                delete window.chrome.runtime.onMessage;
            """
            )

            # Set realistic screen properties
            self.driver.execute_script(
                """
                Object.defineProperty(screen, 'width', {get: () => 1920});
                Object.defineProperty(screen, 'height', {get: () => 1080});
                Object.defineProperty(screen, 'availWidth', {get: () => 1920});
                Object.defineProperty(screen, 'availHeight', {get: () => 1055});
                Object.defineProperty(screen, 'colorDepth', {get: () => 24});
                Object.defineProperty(screen, 'pixelDepth', {get: () => 24});
            """
            )

            # Override user agent via CDP
            self.driver.execute_cdp_cmd(
                "Network.setUserAgentOverride",
                {
                    "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "platform": "macOS",
                },
            )

            logger.info("Stealth scripts applied successfully")

        except Exception as e:
            logger.warning(f"Some stealth scripts failed: {e}")

    def human_like_delay(self, min_seconds=1, max_seconds=3):
        """Add human-like delays"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)

    def visit_vfs_site(self):
        """Visit VFS Global site with stealth approach"""
        try:
            print("🌐 Navigating to VFS Global...")

            # First visit a normal site to establish browsing patterns
            self.driver.get("https://www.google.com")
            self.human_like_delay(2, 4)

            # Then visit VFS Global
            vfs_url = "https://visa.vfsglobal.com/uzb/en/ltp/login/"
            self.driver.get(vfs_url)

            # Wait for page to load naturally
            WebDriverWait(self.driver, 15).until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )

            print("✅ VFS Global site loaded successfully!")

            # Log the success
            self.log_activity(
                "VFS_SITE_LOADED",
                {"url": vfs_url, "title": self.driver.title, "success": True},
            )

            return True

        except Exception as e:
            print(f"❌ Failed to load VFS site: {e}")
            self.log_activity("VFS_SITE_ERROR", str(e))
            return False

    def log_activity(self, activity_type, details):
        """Log activity with timestamp"""
        timestamp = datetime.now()
        activity = {
            "timestamp": timestamp.isoformat(),
            "type": activity_type,
            "details": details,
            "url": self.driver.current_url if self.driver else "N/A",
        }

        self.activity_log.append(activity)
        logger.info(f"Activity: {activity_type} - {details}")

    def monitor_vfs_session(self):
        """Monitor VFS session with stealth"""
        print("\n" + "=" * 60)
        print("🕵️  VFS Global Stealth Monitor Active!")
        print("🔒 Maximum stealth mode engaged")
        print("🌐 You can now login to VFS Global normally")
        print("📝 All activity is being logged")
        print("⏹️  Press Ctrl+C to stop monitoring")
        print("=" * 60)

        last_url = ""

        try:
            while True:
                current_url = self.driver.current_url

                # Check for URL changes
                if current_url != last_url:
                    self.log_activity(
                        "URL_CHANGE", {"from": last_url, "to": current_url}
                    )
                    last_url = current_url

                    # Check for blocking or error pages
                    if (
                        "blocked" in current_url.lower()
                        or "error" in current_url.lower()
                    ):
                        print("⚠️  Possible blocking detected!")
                        self.log_activity("POSSIBLE_BLOCK", current_url)

                # Check if browser is still open
                try:
                    self.driver.current_window_handle
                except:
                    logger.info("Browser window closed by user")
                    break

                # Human-like monitoring interval
                self.human_like_delay(2, 5)

        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Error during monitoring: {str(e)}")

    def save_activity_log(self):
        """Save activity log to file"""
        filename = f"activity_log/vfs_stealth_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
            logger.info(f"VFS activity log saved to: {filename}")
        except Exception as e:
            logger.error(f"Failed to save activity log: {str(e)}")

    def run(self):
        """Main execution method"""
        print("🚀 Starting VFS Global Stealth Monitor...")

        # Setup ultra stealth Chrome
        if not self.setup_ultra_stealth_chrome():
            print("❌ Failed to start stealth browser. Please check your setup.")
            return

        try:
            # Visit VFS site with stealth
            if self.visit_vfs_site():
                # Start monitoring
                self.monitor_vfs_session()
            else:
                print("❌ Could not access VFS Global site")

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
        print("VFS stealth session ended.")


if __name__ == "__main__":
    monitor = VFSStealthMonitor()
    monitor.run()
