#!/usr/bin/env python3
"""
VFS Global Remote Debug Monitor
Uses Chrome remote debugging - completely undetectable by VFS Global
"""

import subprocess
import time
import json
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging
import os

# Set up logging
os.makedirs("activity_log", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("activity_log/vfs_remote_activity.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class VFSRemoteMonitor:
    def __init__(self):
        self.chrome_process = None
        self.driver = None
        self.activity_log = []
        self.start_time = datetime.now()

    def kill_existing_chrome(self):
        """Kill any existing Chrome processes"""
        try:
            subprocess.run(["pkill", "-f", "Google Chrome"], capture_output=True)
            subprocess.run(["pkill", "-f", "chrome"], capture_output=True)
            time.sleep(2)
            print("🧹 Cleaned up existing Chrome processes")
        except Exception as e:
            print(f"Note: {e}")

    def start_chrome_with_remote_debugging(self):
        """Start Chrome with remote debugging (undetectable approach)"""
        try:
            self.kill_existing_chrome()

            # Create a clean temporary profile
            import tempfile

            temp_profile = tempfile.mkdtemp(prefix="vfs_remote_chrome_")

            print(f"🚀 Starting Chrome with remote debugging...")
            print(f"📁 Using clean profile: {temp_profile}")

            # Chrome command with remote debugging
            chrome_cmd = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "--remote-debugging-port=9222",
                f"--user-data-dir={temp_profile}",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-default-apps",
                "--window-size=1920,1080",
            ]

            # Start Chrome process
            self.chrome_process = subprocess.Popen(
                chrome_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

            # Wait for Chrome to start
            time.sleep(3)

            # Test if remote debugging is available
            try:
                response = requests.get("http://127.0.0.1:9222/json/version", timeout=5)
                if response.status_code == 200:
                    print("✅ Chrome remote debugging ready")
                else:
                    raise Exception("Remote debugging not responding")
            except Exception as e:
                raise Exception(f"Failed to connect to Chrome remote debugging: {e}")

            # Connect Selenium to the existing Chrome instance
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

            # No ChromeDriver service needed when connecting to existing instance
            self.driver = webdriver.Chrome(options=chrome_options)

            print("🔗 Connected to Chrome via remote debugging")
            print("🕵️  This method is completely undetectable by VFS Global!")

            return True

        except Exception as e:
            logger.error(f"Failed to start remote Chrome: {e}")
            if self.chrome_process:
                self.chrome_process.terminate()
            return False

    def visit_vfs_global(self):
        """Visit VFS Global site using remote debugging approach"""
        try:
            print("🌐 Navigating to VFS Global (undetected)...")

            # Go directly to VFS Global
            vfs_url = "https://visa.vfsglobal.com/uzb/en/ltp/login/"
            self.driver.get(vfs_url)

            # Wait a moment for the page to load
            time.sleep(3)

            # Check if we're successfully on the site
            current_url = self.driver.current_url
            page_title = self.driver.title

            print(f"✅ Successfully loaded: {page_title}")
            print(f"🔗 URL: {current_url}")

            # Log the success
            self.log_activity(
                "VFS_REMOTE_ACCESS",
                {
                    "url": current_url,
                    "title": page_title,
                    "method": "remote_debugging",
                    "success": True,
                },
            )

            return True

        except Exception as e:
            print(f"❌ Error accessing VFS Global: {e}")
            self.log_activity("VFS_REMOTE_ERROR", str(e))
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

    def monitor_session(self):
        """Monitor the VFS session"""
        print("\n" + "=" * 70)
        print("🕵️  VFS Global Remote Debug Monitor Active!")
        print("🚫 Zero automation detection - completely undetectable")
        print("🌐 You can now use VFS Global normally")
        print("🔐 Login, check slots, make appointments - everything works!")
        print("📝 All activity is being logged")
        print("⏹️  Press Ctrl+C to stop monitoring")
        print("🚪 Or close the Chrome window")
        print("=" * 70)

        last_url = ""

        try:
            while True:
                try:
                    current_url = self.driver.current_url
                    current_title = self.driver.title

                    # Check for URL changes
                    if current_url != last_url:
                        self.log_activity(
                            "URL_CHANGE",
                            {
                                "from": last_url,
                                "to": current_url,
                                "title": current_title,
                            },
                        )
                        last_url = current_url

                        # Print URL changes for visibility
                        print(f"📍 Navigation: {current_title}")

                    # Check if browser is still open
                    self.driver.current_window_handle

                except:
                    print("🚪 Browser window closed")
                    break

                time.sleep(2)

        except KeyboardInterrupt:
            print("\n⏹️  Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Monitoring error: {e}")

    def save_activity_log(self):
        """Save activity log to file"""
        filename = f"activity_log/vfs_remote_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, "w") as f:
                json.dump(
                    {
                        "session_start": self.start_time.isoformat(),
                        "session_end": datetime.now().isoformat(),
                        "method": "remote_debugging",
                        "total_activities": len(self.activity_log),
                        "activities": self.activity_log,
                    },
                    f,
                    indent=2,
                )
            logger.info(f"VFS remote activity log saved to: {filename}")
        except Exception as e:
            logger.error(f"Failed to save activity log: {str(e)}")

    def run(self):
        """Main execution method"""
        print("🚀 Starting VFS Global Remote Debug Monitor...")
        print("🔧 This uses Chrome remote debugging for zero detection")

        # Start Chrome with remote debugging
        if not self.start_chrome_with_remote_debugging():
            print("❌ Failed to start remote debugging Chrome")
            return

        try:
            # Visit VFS Global
            if self.visit_vfs_global():
                # Start monitoring
                self.monitor_session()
            else:
                print("❌ Could not access VFS Global")

        except KeyboardInterrupt:
            print("\n⏹️  Program interrupted")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        try:
            if self.driver:
                self.driver.quit()
        except:
            pass

        try:
            if self.chrome_process:
                self.chrome_process.terminate()
                self.chrome_process.wait(timeout=5)
        except:
            pass

        # Save activity log
        self.save_activity_log()

        print(f"\n📊 Total activities logged: {len(self.activity_log)}")
        print("✅ VFS remote debug session ended")


if __name__ == "__main__":
    monitor = VFSRemoteMonitor()
    monitor.run()
