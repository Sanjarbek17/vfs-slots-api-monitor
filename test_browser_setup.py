#!/usr/bin/env python3
"""
Quick test script to verify the browser setup works
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from browser_monitor import BrowserMonitor


def test_browser_setup():
    """Test if browser setup works without errors"""
    print("Testing browser setup...")

    monitor = BrowserMonitor()

    if monitor.setup_chrome():
        print("✅ Browser setup successful!")
        print(f"✅ Browser version: {monitor.driver.capabilities['browserVersion']}")
        print(
            f"✅ Driver version: {monitor.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]}"
        )

        # Test basic navigation
        try:
            monitor.driver.get("https://httpbin.org/get")
            print("✅ Basic navigation test successful!")
            print(f"✅ Current URL: {monitor.driver.current_url}")
        except Exception as e:
            print(f"❌ Navigation test failed: {e}")

        monitor.cleanup()
        return True
    else:
        print("❌ Browser setup failed!")
        return False


if __name__ == "__main__":
    success = test_browser_setup()
    sys.exit(0 if success else 1)
