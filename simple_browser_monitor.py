#!/usr/bin/env python3
"""
Simple Browser Monitor - Basic version
Opens Chrome, lets you enter URLs, and logs basic interactions.
"""

import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class SimpleBrowserMonitor:
    def __init__(self):
        self.driver = None
        self.activities = []

    def setup_browser(self):
        """Setup Chrome browser"""
        print("Setting up Chrome browser...")

        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        print("✅ Browser ready!")

    def log_activity(self, activity):
        """Log an activity with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {activity}"
        self.activities.append(log_entry)
        print(log_entry)

    def get_url(self):
        """Get URL from user input"""
        url = input("\n🌐 Enter URL to visit (or 'quit' to exit): ").strip()

        if url.lower() == "quit":
            return None

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        return url

    def monitor_activity(self):
        """Monitor basic browser activity"""
        print("\n" + "=" * 50)
        print("🔍 Monitoring your browser activity...")
        print("You can now interact with the browser normally.")
        print("Press Ctrl+C here to stop monitoring.")
        print("=" * 50)

        last_url = ""
        last_title = ""

        try:
            while True:
                # Check current state
                current_url = self.driver.current_url
                current_title = self.driver.title

                # Log URL changes
                if current_url != last_url:
                    self.log_activity(f"📍 URL changed to: {current_url}")
                    last_url = current_url

                # Log title changes
                if current_title != last_title and current_title:
                    self.log_activity(f"📄 Page title: {current_title}")
                    last_title = current_title

                # Check if browser is still open
                try:
                    self.driver.current_window_handle
                except:
                    self.log_activity("❌ Browser window was closed")
                    break

                time.sleep(1)  # Check every second

        except KeyboardInterrupt:
            self.log_activity("⏹️  Monitoring stopped by user")

    def run(self):
        """Main program loop"""
        print("🚀 Starting Simple Browser Monitor")

        try:
            self.setup_browser()

            while True:
                url = self.get_url()
                if url is None:
                    break

                self.log_activity(f"🔗 Navigating to: {url}")
                self.driver.get(url)

                # Start monitoring
                self.monitor_activity()

                # Ask to continue
                if input("\n➡️  Visit another URL? (y/n): ").lower() != "y":
                    break

        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                print("✅ Browser closed")

            # Save activity log
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"simple_activity_{timestamp}.txt"
            with open(filename, "w") as f:
                f.write("\n".join(self.activities))
            print(f"📁 Activity saved to: {filename}")


if __name__ == "__main__":
    monitor = SimpleBrowserMonitor()
    monitor.run()
